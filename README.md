# Second Brain for VS Code Copilot

An Obsidian vault that GitHub Copilot (with Claude models) reads before a task and
updates after it, so Jira tickets, Confluence knowledge and decisions stay linked across
chats and projects.

## What's in this repo

| Path | What it is | Where it goes |
|---|---|---|
| `.github/skills/second-brain/SKILL.md` | The rulebook: vault layout, linking rules, Recall / Log / Connect / Capture modes | `~/.copilot/skills/second-brain/SKILL.md` (all projects) or a project's `.github/skills/second-brain/` |
| `copilot-user-prompts/second-brain.instructions.md` | Always-on rules, added to every message: *when* to use the vault | VS Code user prompts folder |
| `copilot-user-prompts/*.prompt.md` | Slash commands `/recall`, `/log`, `/connect`, `/capture` | VS Code user prompts folder |
| `vault-template/` | Empty vault: folders, note templates, `Home.md` | Copy to e.g. `~/Documents/Second-Brain` and open in Obsidian |
| `tools/link_doctor.py` | Optional link checker you can run by hand. The skill never runs it. | Anywhere |

The instructions file says **when** to use the second brain; `SKILL.md` says **how**.

## Setup

1. **Vault:** copy `vault-template/` to `~/Documents/Second-Brain`. In Obsidian choose
   *Open folder as vault*. Turn on core plugins **Templates** (folder `Templates`, date
   `YYYY-MM-DD`) and **Daily notes** (folder `Daily`, template `Templates/daily`), and
   *Files and links > Automatically update internal links*.
2. **Skill:** copy `.github/skills/second-brain/SKILL.md` to
   `~/.copilot/skills/second-brain/SKILL.md`.
3. **Instructions and commands:** copy the five files in `copilot-user-prompts/` to the
   VS Code user prompts folder:
   - macOS: `~/Library/Application Support/Code/User/prompts`
   - Windows: `%APPDATA%\Code\User\prompts`
   - Linux: `~/.config/Code/User/prompts`

   Or run **Chat: New Prompt File > User Data** to have VS Code open that folder.
   Then open `second-brain.instructions.md` and put your vault path on the
   *Vault location* line.
4. **Workspace:** in your project, *File > Add Folder to Workspace*, pick the vault,
   then *Save Workspace As*. Open that `.code-workspace` file from now on.
5. **Test:** Copilot chat in **Agent** mode with a **Claude** model:
   `/capture` a ticket, `/recall` it, `/log`, then open Obsidian's graph view.

If a command doesn't appear, older VS Code uses `mode: agent` instead of `agent: agent`
at the top of the `.prompt.md` files.

## Daily use

| When | Type |
|---|---|
| Starting a ticket | `/recall PROJ-1234` |
| Got a ticket or Confluence page to keep | `/capture` + paste |
| Finished a piece of work | `/log` |
| Once a week | `/connect` |

Model tip: Sonnet for `/recall`, `/log`, `/capture`; Opus for the weekly `/connect`.

## Safety rules built into the skill

- Asks where the vault is before reading or writing anything; never guesses.
- Never runs terminal commands or scripts; file tools only.
- Never deletes files, never stores secrets, asks before merging notes.
