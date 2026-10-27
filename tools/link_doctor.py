#!/usr/bin/env python3
"""
link_doctor.py - find and fix missing links in an Obsidian vault.

Usage (from the vault root):
    python tools/link_doctor.py .            # report only
    python tools/link_doctor.py . --fix      # apply safe fixes
    python tools/link_doctor.py . --keys PROJ,PAY   # only these Jira projects

What it checks:
  * unlinked mentions   - text that matches an existing note name/alias or a Jira key, not in [[ ]]
  * broken links        - [[links]] to notes that don't exist
  * missing tickets     - Jira keys mentioned anywhere that have no note in Tickets/
  * orphans             - notes nothing links to
  * duplicate names     - notes whose names differ only by case/spaces/punctuation

What --fix does (safe, never deletes):
  * wraps the first unlinked mention of each note per file in [[ ]]
  * normalises Jira keys like "proj 1234" only when --keys is given
  * creates stub notes in Tickets/ for missing tickets (from Templates/ticket.md)

Standard library only. Works on Windows, macOS and Linux (Python 3.8+).
"""
from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from collections import defaultdict
from pathlib import Path

SKIP_DIRS = {".obsidian", ".git", ".github", ".trash", "Templates", "Skills", "node_modules"}
NEVER_LINK_IN = {"Home"}  # notes we don't auto-edit for mentions
MIN_NAME_LEN = 4
COMMON_WORDS = {  # note names too generic to auto-link
    "home", "inbox", "todo", "notes", "readme", "index", "daily", "log", "work",
    "test", "tests", "ticket", "tickets", "project", "projects", "people", "knowledge",
    "decisions", "decision", "related", "summary", "status", "next", "done",
}
JIRA_IGNORE = {"UTF", "SHA", "ISO", "RFC", "TLS", "SSL", "HTTP", "COVID", "CVE", "MD", "AES", "RSA", "IPV", "X"}

LINK_RE = re.compile(r"!?\[\[([^\]\|#]+)(#[^\]\|]*)?(\|[^\]]*)?\]\]")
MDLINK_RE = re.compile(r"\[[^\]]*\]\([^)]*\)")
URL_RE = re.compile(r"https?://\S+")
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1[^\n]*$", re.S | re.M)
FRONTMATTER_RE = re.compile(r"\A---\n.*?\n---\n", re.S)
TAG_RE = re.compile(r"(?<!\w)#[\w/-]+")


def norm(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


def parse_aliases(text: str) -> list[str]:
    m = FRONTMATTER_RE.match(text)
    if not m:
        return []
    fm = m.group(0)
    out: list[str] = []
    inline = re.search(r"^aliases:\s*\[(.*?)\]\s*$", fm, re.M)
    if inline:
        out += [a.strip().strip("'\"") for a in inline.group(1).split(",") if a.strip()]
    block = re.search(r"^aliases:\s*\n((?:\s+-\s+.*\n)+)", fm, re.M)
    if block:
        out += [l.strip()[1:].strip().strip("'\"") for l in block.group(1).splitlines() if l.strip()]
    return [a for a in out if a]


def protected_spans(text: str, include_links: bool = True) -> list[tuple[int, int]]:
    spans = []
    m = FRONTMATTER_RE.match(text)
    if m:
        spans.append((0, m.end()))
    rxs = (FENCE_RE, INLINE_CODE_RE, LINK_RE, MDLINK_RE, URL_RE, TAG_RE) if include_links \
        else (FENCE_RE, INLINE_CODE_RE, MDLINK_RE, URL_RE)
    for rx in rxs:
        spans += [(x.start(), x.end()) for x in rx.finditer(text)]
    spans.sort()
    merged: list[list[int]] = []
    for s, e in spans:
        if merged and s <= merged[-1][1]:
            merged[-1][1] = max(merged[-1][1], e)
        else:
            merged.append([s, e])
    return [(s, e) for s, e in merged]


def in_spans(pos: int, end: int, spans: list[tuple[int, int]]) -> bool:
    for s, e in spans:
        if s > end:
            return False
        if s < end and pos < e:
            return True
    return False


class Vault:
    def __init__(self, root: Path, keys: set[str] | None):
        self.root = root
        self.keys = keys
        self.notes: dict[str, Path] = {}          # lower name -> path
        self.names: dict[str, str] = {}           # lower name -> real name
        self.alias_to: dict[str, str] = {}        # lower alias -> real note name
        self.texts: dict[Path, str] = {}
        self.load()
        jira_core = r"[A-Z][A-Z0-9]{1,9}-\d{1,6}"
        if keys:
            self.jira_re = re.compile(r"\b(" + "|".join(map(re.escape, sorted(keys))) + r")[\s_-]?(\d{1,6})\b", re.I)
        else:
            self.jira_re = re.compile(r"\b(" + jira_core + r")\b")

    def load(self):
        for p in sorted(self.root.rglob("*.md")):
            rel = p.relative_to(self.root)
            if any(part in SKIP_DIRS or part.startswith(".") for part in rel.parts[:-1]):
                continue
            text = p.read_text(encoding="utf-8", errors="replace").replace("\r\n", "\n")
            self.texts[p] = text
            self.notes[p.stem.lower()] = p
            self.names[p.stem.lower()] = p.stem
        for p, text in self.texts.items():
            for a in parse_aliases(text):
                self.alias_to.setdefault(a.lower(), p.stem)

    def resolve(self, target: str) -> str | None:
        t = target.strip().split("/")[-1]
        if t.lower().endswith(".md"):
            t = t[:-3]
        if t.lower() in self.notes:
            return self.names[t.lower()]
        if t.lower() in self.alias_to:
            return self.alias_to[t.lower()]
        return None

    def jira_keys_in(self, text: str) -> list[tuple[int, int, str]]:
        out = []
        for m in self.jira_re.finditer(text):
            if self.keys:
                key = f"{m.group(1).upper()}-{m.group(2)}"
            else:
                key = m.group(1)
                if key.split("-")[0] in JIRA_IGNORE:
                    continue
            out.append((m.start(), m.end(), key))
        return out


def build_mention_regex(vault: Vault) -> tuple[re.Pattern | None, dict[str, str]]:
    terms: dict[str, str] = {}
    for low, real in vault.names.items():
        if len(real) >= MIN_NAME_LEN and low not in COMMON_WORDS and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", real):
            terms[low] = real
    for alias_low, real in vault.alias_to.items():
        if len(alias_low) >= MIN_NAME_LEN and alias_low not in COMMON_WORDS:
            terms.setdefault(alias_low, real)
    if not terms:
        return None, terms
    alts = sorted(terms, key=len, reverse=True)
    rx = re.compile(r"(?<![\w\[/-])(" + "|".join(re.escape(t) for t in alts) + r")(?![\w\]/-])", re.I)
    return rx, terms


def analyse(vault: Vault):
    mention_rx, terms = build_mention_regex(vault)
    incoming: dict[str, set[str]] = defaultdict(set)
    broken: dict[str, set[str]] = defaultdict(set)
    unlinked: dict[Path, list[tuple[int, int, str, str]]] = defaultdict(list)
    tickets_mentioned: dict[str, set[str]] = defaultdict(set)

    for p, text in vault.texts.items():
        code_only = protected_spans(text, include_links=False)
        for m in LINK_RE.finditer(text):
            if in_spans(m.start(), m.end(), code_only):
                continue  # [[...]] inside `code` or a code block is not a link
            target = m.group(1)
            if not target.strip() or re.fullmatch(r"\s*\d{4}-\d{2}-\d{2}\s*", target):
                continue  # empty template link, or a daily note not written yet
            real = vault.resolve(target)
            if real:
                if real != p.stem:
                    incoming[real].add(p.stem)
            elif not re.search(r"\.(png|jpe?g|gif|svg|pdf|webp|excalidraw|canvas)$", target, re.I):
                broken[target.strip()].add(p.stem)

        spans = protected_spans(text)
        code_spans = protected_spans(text, include_links=False)
        body_start = FRONTMATTER_RE.match(text).end() if FRONTMATTER_RE.match(text) else 0

        for s, e, key in vault.jira_keys_in(text):
            if s < body_start or in_spans(s, e, code_spans):
                continue  # frontmatter, code blocks and URLs are not real mentions
            tickets_mentioned[key].add(p.stem)
            if key == p.stem or in_spans(s, e, spans):
                continue
            unlinked[p].append((s, e, key, text[s:e]))

        if mention_rx and p.stem not in NEVER_LINK_IN:
            for m in mention_rx.finditer(text):
                s, e = m.span()
                real = terms[m.group(1).lower()]
                if real == p.stem or in_spans(s, e, spans):
                    continue
                if any(not (e <= us or s >= ue) for us, ue, _, _ in unlinked[p]):
                    continue
                unlinked[p].append((s, e, real, m.group(1)))

    missing_tickets = {k: srcs for k, srcs in tickets_mentioned.items() if k.lower() not in vault.notes}
    for k in list(broken):
        if vault.jira_re.fullmatch(k) and k.upper() not in missing_tickets:
            missing_tickets.setdefault(k.upper(), set()).update(broken[k])

    orphans = sorted(
        name for low, name in vault.names.items()
        if name not in incoming and name not in NEVER_LINK_IN
        and not str(vault.notes[low].relative_to(vault.root)).startswith("Daily")
    )
    groups: dict[str, list[str]] = defaultdict(list)
    for name in vault.names.values():
        groups[norm(name)].append(name)
    dupes = [sorted(v) for v in groups.values() if len(v) > 1]
    return unlinked, broken, missing_tickets, orphans, dupes


def apply_fixes(vault: Vault, unlinked) -> int:
    changed = 0
    for p, hits in unlinked.items():
        text = vault.texts[p]
        seen: set[str] = set()
        edits = []
        for s, e, target, shown in sorted(hits):
            if target in seen:
                continue
            seen.add(target)
            link = f"[[{target}]]" if shown == target else f"[[{target}|{shown}]]"
            if vault.keys and re.fullmatch(r"[A-Z0-9]+-\d+", target) and shown != target:
                link = f"[[{target}]]"  # normalise "proj 1234" -> [[PROJ-1234]]
            edits.append((s, e, link))
        for s, e, link in sorted(edits, reverse=True):
            text = text[:s] + link + text[e:]
        if edits:
            p.write_text(text, encoding="utf-8")
            vault.texts[p] = text
            changed += len(edits)
    return changed


def create_stubs(vault: Vault, missing: dict[str, set[str]]) -> list[str]:
    tmpl_path = vault.root / "Templates" / "ticket.md"
    tmpl = tmpl_path.read_text(encoding="utf-8") if tmpl_path.exists() else "# {{title}}\n"
    today = dt.date.today().isoformat()
    created = []
    (vault.root / "Tickets").mkdir(exist_ok=True)
    for key, sources in sorted(missing.items()):
        dest = vault.root / "Tickets" / f"{key}.md"
        if dest.exists():
            continue
        body = tmpl.replace("{{title}}", key).replace("{{date}}", today)
        body = body.replace("{{date:YYYY-MM-DD}}", today)
        body += "\n> Stub created by link_doctor. Mentioned in: " + ", ".join(f"[[{s}]]" for s in sorted(sources)) + "\n"
        dest.write_text(body, encoding="utf-8")
        created.append(key)
    return created


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("vault", nargs="?", default=".", help="vault root folder (default: current folder)")
    ap.add_argument("--fix", action="store_true", help="apply safe fixes")
    ap.add_argument("--keys", help="comma-separated Jira project keys, e.g. PROJ,PAY")
    args = ap.parse_args()

    root = Path(args.vault).resolve()
    if not root.is_dir():
        print(f"Not a folder: {root}", file=sys.stderr)
        return 2
    keys = {k.strip().upper() for k in args.keys.split(",")} if args.keys else None
    vault = Vault(root, keys)
    unlinked, broken, missing, orphans, dupes = analyse(vault)

    print(f"# Link doctor report - {root.name} ({len(vault.texts)} notes)\n")
    n_unlinked = sum(len({t for _, _, t, _ in v}) for v in unlinked.values())
    print(f"## Unlinked mentions: {n_unlinked}")
    for p, hits in sorted(unlinked.items()):
        targets = sorted({t for _, _, t, _ in hits})
        print(f"- {p.relative_to(root)}: " + ", ".join(f"[[{t}]]" for t in targets))
    print(f"\n## Broken links: {len(broken)}")
    for t, srcs in sorted(broken.items()):
        print(f"- [[{t}]] in " + ", ".join(sorted(srcs)))
    print(f"\n## Tickets with no note: {len(missing)}")
    for k, srcs in sorted(missing.items()):
        print(f"- {k} (mentioned in " + ", ".join(sorted(srcs)) + ")")
    print(f"\n## Orphans (nothing links here): {len(orphans)}")
    for o in orphans:
        print(f"- [[{o}]]")
    print(f"\n## Possible duplicates: {len(dupes)}")
    for d in dupes:
        print("- " + " / ".join(f"[[{x}]]" for x in d))

    if args.fix:
        n = apply_fixes(vault, unlinked)
        stubs = create_stubs(vault, missing)
        print(f"\n## Fixed\n- links added: {n}\n- ticket stubs created: {len(stubs)}" +
              (f" ({', '.join(stubs)})" if stubs else ""))
        print("- broken links, orphans and duplicates need judgement: handle them in chat")
    else:
        print("\nRun again with --fix to add the missing links and ticket stubs.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
