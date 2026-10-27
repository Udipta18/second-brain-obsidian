---
name: second-brain
description: Long-term memory in an Obsidian vault (second brain). Use to recall past work, log a chat session, connect missing links, or capture a Jira ticket, Confluence page, decision or project into notes. Triggers - recall, remember, log, save, note, second brain, vault, Obsidian, Jira, ticket, Confluence, link, connect, what did I do.
---

# Second brain (Obsidian vault)

The vault is a folder of Markdown files. Obsidian draws the graph from `[[wikilinks]]`,
so **every useful fact must be linked to the notes it belongs to**. Your job is to keep
the vault complete, consistent and connected.

## Ground rules (read first, always follow)

### 1. Never run commands

This runs on an office laptop where running commands is not expected.

- **Do not run any terminal, shell, Python, script, git or package command.** Not to
  read files, not to check the date, not to find the vault, not "just once".
- Use **only** the editor's file tools: read file, list folder, search files, create file,
  edit file.
- If something can only be done with a command, don't do it. Say what you would need
  and ask the user to do it or to give you the information.

### 2. Find out where the vault is before doing anything

Before reading or writing any note:

1. Check whether the user already told you the vault folder in this chat or in the
   always-on instructions. If yes, use it.
2. Otherwise, look at the open workspace folders for one that contains `Home.md` and the
   folders `Daily/`, `Tickets/`, `Projects/`. If exactly one matches, tell the user in one
   line which folder you'll use (e.g. "Using the vault at `Second-Brain/`").
3. If none or more than one matches, **stop and ask**:
   > "Where is your Obsidian vault? Please give me the folder path (for example
   > `~/Documents/Second-Brain`), or add the vault folder to this workspace."
   Don't guess, don't search the whole disk, don't create a new vault on your own.
4. If the folder the user gives is not open in the workspace and you can't read it,
   ask them to add it via **File > Add Folder to Workspace**, then continue.

All paths below are relative to the vault root.

### 3. Get today's date without commands

Use the date from the conversation or the editor context. If you don't know it for sure,
ask the user ("What's today's date?") before creating a daily note or dated decision.

## Vault layout

| Folder | One note per | File name | Template |
|---|---|---|---|
| `Daily/` | day | `YYYY-MM-DD.md` | `Templates/daily.md` |
| `Tickets/` | Jira ticket | `PROJ-1234.md` (exact Jira key) | `Templates/ticket.md` |
| `Projects/` | project, repo or service | `Payments Service.md` | `Templates/project.md` |
| `Knowledge/` | Confluence page, how-to, concept | `Staging Deploy Guide.md` | `Templates/knowledge.md` |
| `Decisions/` | decision and its reason | `2026-10-27 Use retry with backoff.md` | `Templates/decision.md` |
| `People/` | colleague you work with | `Firstname Lastname.md` | none, a short bio |
| `Inbox/` | anything unsorted | any | none |

`Home.md` is the map of the whole vault. Keep its lists of projects up to date.
Ignore the `Templates/` and `Skills/` folders when looking for notes.

## Naming and linking rules (the most important part)

1. **One name, one note.** Before creating a note, search the vault for an existing one
   (file names, `aliases:` in frontmatter, and headings). Reuse it. Never create
   `PROJ 1234.md` next to `PROJ-1234.md`.
2. **Jira keys are always uppercase with a hyphen**: `[[PROJ-1234]]`. Normalise
   `proj1234`, `PROJ 1234`, `ticket 1234` to that form.
3. **Link on every mention** of a ticket, project, knowledge note, decision or person:
   `[[PROJ-1234]]`, `[[Payments Service]]`. Use an alias when the sentence needs it:
   `[[Payments Service|payments]]`.
4. **Every note links upwards**: a ticket links its project; a decision links the
   ticket or project it was made for; a knowledge note links the projects it applies to;
   a project is listed in `Home.md`. No note should be an orphan.
5. **Daily notes are the timeline.** Each work entry in a daily note links the ticket or
   project, and the ticket or project gets a back-entry under `## Log` that links
   the day: `- [[2026-10-27]]: fixed TTL, see [[2026-10-27 Raise session TTL]]`.
6. When a project has another common name, add it to `aliases:` so future mentions match.
7. Use `tags:` only for type and status (`type/ticket`, `status/in-progress`). Use links,
   not tags, for relationships.
8. **Never store secrets** (passwords, tokens, keys, connection strings) or customer
   personal data. Write `<redacted>` instead.

## Modes

Pick the mode from what the user asked. When unsure, ask in one line.
Every mode starts with the ground rules above: no commands, and the vault folder known.

### 1. Recall ("what do I know about…", start of a task)

1. Identify the ticket key, project or topic from the request, the open files or the
   workspace folder name. If it's still unclear, ask the user which ticket or project.
2. Search the vault for it and read the matching note, then follow its links one level
   out (project, related tickets, knowledge, decisions) and the last 3 daily entries
   that link to it.
3. Reply with a short briefing: current status, what was done, open questions,
   steps that worked, relevant docs. Cite the notes as `[[links]]`.
4. If nothing exists yet, say so and offer to create the ticket or project note.

### 2. Log ("log this", "save this session", end of a task)

1. Summarise this chat session: goal, what was done, root cause or findings,
   decisions and why, steps or commands the user ran that worked, open questions,
   next step.
2. Append to `Daily/<today>.md` (create from template if missing) under `## Work log`:

   ```markdown
   ### [[PROJ-1234]] Login timeout fix
   - Project: [[Payments Service]]
   - Done: raised session TTL from 5 to 30 min in `config/session.yml`
   - Why: users timed out mid-checkout, see [[2026-10-27 Raise session TTL]]
   - Used: [[Staging Deploy Guide]]
   - Next: QA sign-off
   ```

3. Update the ticket note: status in frontmatter, a dated line under `## Log` linking the
   day, and any new acceptance criteria or validation steps.
4. Create a `Decisions/` note for any real decision (an option chosen over another).
5. Create or update a `Knowledge/` note for any reusable how-to learned in the session
   (a sequence of steps, a gotcha, an environment detail).
6. Run **Connect** on the notes you touched only (not the whole vault).
7. Reply with the list of notes created or changed, as `[[links]]`.

### 3. Connect ("connect my notes", "fix missing links", weekly clean-up)

Goal: no unlinked mentions, no broken links, no orphans, no duplicates.
Do all of this by reading and editing notes with file tools. **Do not run the
`link_doctor.py` script** in `Skills/`; it is only for the user to run by hand
outside the office, if they choose to.

1. **List what exists:** list the files in `Tickets/`, `Projects/`, `Knowledge/`,
   `Decisions/` and `People/`, and note each file name plus any `aliases:` in its
   frontmatter. This is the list of names to link.
2. **Unlinked mentions:** search the notes for those names, aliases and Jira keys
   (`[A-Z]+-[0-9]+`) where they are not inside `[[ ]]`. Wrap the first mention in each
   note in `[[ ]]`. Never link inside code blocks, inline code, URLs, frontmatter or
   headings, and never link a note to itself.
3. **Missing tickets:** a Jira key mentioned somewhere with no note in `Tickets/` →
   create a stub from `Templates/ticket.md` with what you know and
   `> Stub created by second-brain. Mentioned in: [[...]]`.
4. **Broken links:** a `[[link]]` to a note that doesn't exist → fix the spelling to
   match the existing note, or create the note from the right template.
5. **Orphans:** a note nothing links to → link it from its project, ticket, today's
   daily note or `Home.md`.
6. **Semantic links:** for each note touched, look for notes about the same topic that
   aren't linked yet: same error message, same service, same Confluence space, same
   person, same component. Add them under `## Related` with a short reason:
   `- [[PROJ-1180]] same timeout in the auth service`.
7. **Duplicates:** if two notes are about the same thing, propose a merge and **ask
   before merging**. When approved, keep the correct name, move the content there, add
   the other name to `aliases:`, and replace the duplicate's body with
   `Moved to [[Correct Name]]`. Never delete files.
8. Update `Home.md` with any new project.
9. Reply with a summary: links added, stubs created, broken links fixed, orphans
   fixed, duplicates found.

For a large vault, do it in batches (one folder at a time) and tell the user which
folders are done.

### 4. Capture ("save this ticket", "summarise this Confluence page")

- **Jira ticket** (pasted text or details from chat): create `Tickets/<KEY>.md` from the
  template. Fill summary, acceptance criteria, validation steps, links to project and
  people. Keep the Jira URL in `jira:` frontmatter.
- **Confluence page** (pasted text): create `Knowledge/<Page Title>.md` from the
  template. Write a summary in your own words, the exact steps, gotchas, and the page URL
  in `source:`. Link it to the projects and tickets it applies to.
- **Decision**: create `Decisions/<YYYY-MM-DD> <short title>.md` from the template.
- **A whole chat**: create or update the project note, add Knowledge and Decision notes
  for what was learned and decided, and a daily entry linking them all.
- After capturing, run Connect steps 2-6 on the new notes.

## Editing rules

- Append, don't rewrite. Keep the user's own text exactly as it is.
- Keep frontmatter valid YAML. Dates are `YYYY-MM-DD`.
- Keep entries short: bullets, not essays. The graph and links carry the structure.
- Never delete files. Never write outside the vault folder.
