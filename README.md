# 🧠 Second Brain for VS Code Copilot

![Copilot](https://img.shields.io/badge/GitHub%20Copilot-VS%20Code-0078D4?style=for-the-badge&logo=visualstudiocode&logoColor=white)
![Obsidian](https://img.shields.io/badge/Obsidian-Vault-7C3AED?style=for-the-badge&logo=obsidian&logoColor=white)
![No commands](https://img.shields.io/badge/Runs%20commands-Never-2EA043?style=for-the-badge)
![Windows](https://img.shields.io/badge/Windows-Ready-F2541B?style=for-the-badge&logo=windows&logoColor=white)

$\color{#f2541b}{\textsf{\textbf{Goldfish memory in, long-term memory out.}}}$

AI chats have goldfish memory: every new Copilot chat starts from zero. This repo gives
Copilot a long-term memory in an **Obsidian vault**. Copilot reads the vault before a
task and writes to it after, so Jira tickets, Confluence knowledge and decisions stay
linked across chats and projects, the way neurons link memories in a brain.

- 🔵 Works with **GitHub Copilot in VS Code** (Agent mode, Claude model)
- 🟣 Notes are plain Markdown files on your own laptop: no server, no database
- 🟢 The skill **never runs terminal commands** and **asks where your vault is** if it can't find it

---

## 📦 What's in this repo

| Path | What it is | Needed? |
|---|---|---|
| `.github/skills/second-brain/SKILL.md` | The rulebook: vault layout, linking rules, the four modes | ✅ **Yes** |
| `copilot-user-prompts/second-brain.instructions.md` | Always-on rules: tells Copilot *when* to use the vault | ✅ **Yes** |
| `copilot-user-prompts/recall.prompt.md` | `/recall` command | ⚪ Optional |
| `copilot-user-prompts/log.prompt.md` | `/log` command | ⚪ Optional |
| `copilot-user-prompts/capture.prompt.md` | `/capture` command | ⚪ Optional |
| `copilot-user-prompts/connect.prompt.md` | `/connect` command | ⚪ Optional |
| `vault-template/` | Folders, note templates and `Home.md` | ⚪ Optional (an empty folder works) |
| `presentation/second-brain-talk.html` | 10-slide talk explaining the idea | 🟠 For presenting |
| `tools/link_doctor.py` | Link checker you can run by hand. The skill never runs it | ⚪ Optional |

> [!IMPORTANT]
> The instructions file says **when** to use the second brain. `SKILL.md` says **how**. Only these two files are required.

---

## 🟦 Setup on Windows (about 10 minutes)

> [!TIP]
> You only copy and paste text from GitHub. Nothing to download or install except Obsidian.

### 🟦 Step 1: Make the vault

1. In **File Explorer**, go to **Documents** and create a folder called `Second-Brain`.
2. Open **Obsidian**, click **Open folder as vault**, and pick `Second-Brain`.
3. In Obsidian, go to **Settings > Files and links** and turn on
   **Automatically update internal links**.
4. Right-click the `Second-Brain` folder in File Explorer and choose **Copy as path**
   (Windows 10: hold **Shift** while right-clicking). Keep this path for Step 3.
   It may be inside OneDrive, so use the copied path rather than guessing.

### 🟪 Step 2: Install the skill

1. Open [SKILL.md](.github/skills/second-brain/SKILL.md) on GitHub and click the
   **Copy raw file** icon (two overlapping squares) above the text.
2. In VS Code, click **File > Open Folder**. In the address bar of the window that
   opens, type `%USERPROFILE%`, press **Enter**, then click **Select Folder**.
   This opens your user folder (`C:\Users\<you>`). Click **Yes, I trust the authors** if asked.
3. In the **Explorer** panel on the left, hover over the folder name and click the
   **New File** icon. Type this exactly and press **Enter**:

   ```
   .copilot/skills/second-brain/SKILL.md
   ```

   VS Code creates the folders and opens an empty file.
4. Click inside the file, press **Ctrl+V**, then **Ctrl+S**.
5. Go back to your project with **File > Open Recent**.

> [!NOTE]
> **Shortcut for one project only:** open your project, click **New File**, type
> `.github/skills/second-brain/SKILL.md`, paste and save. Don't commit it to your team's repo.

### 🟧 Step 3: Install the instructions

1. Open [second-brain.instructions.md](copilot-user-prompts/second-brain.instructions.md)
   on GitHub and click **Copy raw file**.
2. In VS Code, press **Ctrl+Shift+P**, type `Chat: New Instructions File`, press **Enter**.
3. Choose **User Data**, type the name `second-brain`, press **Enter**.
4. Press **Ctrl+A**, then **Ctrl+V**.
5. Find the line `- **Vault location:**` and replace the comment
   `<!-- put your vault path here ... -->` with the path you copied in Step 1
   (remove the quotation marks).
6. Press **Ctrl+S**.

### 🟩 Step 4: Add the four commands (optional, recommended)

Repeat for each row:

| Name to type | Copy from |
|---|---|
| `recall` | [recall.prompt.md](copilot-user-prompts/recall.prompt.md) |
| `log` | [log.prompt.md](copilot-user-prompts/log.prompt.md) |
| `capture` | [capture.prompt.md](copilot-user-prompts/capture.prompt.md) |
| `connect` | [connect.prompt.md](copilot-user-prompts/connect.prompt.md) |

1. Open the file on GitHub and click **Copy raw file**.
2. In VS Code, press **Ctrl+Shift+P**, run `Chat: New Prompt File`, choose **User Data**.
3. Type the name from the table and press **Enter**.
4. Press **Ctrl+A**, **Ctrl+V**, **Ctrl+S**.

Type `/` in the Copilot chat box: all four should appear.

### 🟨 Step 5: Connect the vault to your project

1. Open your project in VS Code.
2. Click **File > Add Folder to Workspace** and pick `Second-Brain`.
3. The Explorer panel now shows two folders: your project and `Second-Brain`.

If VS Code asks to save the workspace, you can ignore it. If it ever forgets the vault,
repeat this step.

### ✅ Step 6: Test it

1. Open Copilot chat (**Ctrl+Alt+I**), set the mode to **Agent** and pick a **Claude** model.
2. Type:

   ```
   /capture PAY-1: login times out after 5 minutes
   ```

3. Click **Keep** on the file edits. A note `Tickets/PAY-1.md` appears in Obsidian.
4. Type `/recall PAY-1`, then `/log`.
5. In Obsidian, click the **graph view** icon in the left sidebar to see the linked notes.

> [!WARNING]
> Use a made-up ticket for the first test, not real customer data.

---

## 🍎 Setup on Mac

Same steps, with these differences:

| Windows | Mac |
|---|---|
| `Ctrl` | `Cmd` |
| File Explorer, **Copy as path** | Finder, right-click the folder, hold **Option**, **Copy as Pathname** |
| **File > Open Folder**, type `%USERPROFILE%` | **File > Open...**, press **Cmd+Shift+H**, click **Open** |
| `C:\Users\<you>\Documents\Second-Brain` | `~/Documents/Second-Brain` |

---

## 🟢 How to use it

| Command | When | Example | What you get |
|---|---|---|---|
| `/capture` | A new ticket or Confluence page | `/capture Jira PAY-1300: Refund webhook times out after 10s. Done when it replies in 2s and retries. Reporter: Priya Sharma.` | A linked note in `Tickets/` or `Knowledge/` |
| `/recall` | Starting or restarting a ticket | `/recall PAY-1300` | A briefing: status, what was tried, open questions, related notes |
| `/log` | Finished a fix, test or decision | `/log` or `/log We chose async refunds because the gateway caps timeouts at 10s` | Today's `Daily/` entry, ticket log updated, a `Decisions/` note if you chose between options |
| `/connect` | Once a week | `/connect` | Missing links added, ticket notes created for plain-text mentions, related notes linked |

Without the commands, plain words work too:
`Use the second-brain skill to log this session`.

**A normal day:** `/capture` new tickets, `/recall` before you start, `/log` when you finish,
`/connect` on Friday.

**Which model:** Sonnet for `/recall`, `/log`, `/capture`. Opus for the weekly `/connect`,
since it's better at spotting related notes.

---

## 🟣 Vault layout

| Folder | One note per | Example |
|---|---|---|
| `Daily/` | day (the timeline) | `2026-10-27.md` |
| `Tickets/` | Jira ticket | `PAY-1234.md` |
| `Projects/` | service or repo | `Payments Service.md` |
| `Knowledge/` | Confluence page or how-to | `Staging Deploy Guide.md` |
| `Decisions/` | choice and its reason | `2026-10-27 Async refunds.md` |
| `People/` | colleague | `Priya Sharma.md` |
| `Inbox/` | anything unsorted | `Standup notes.md` |

The skill creates missing folders itself, so an empty vault folder is enough to start.
`vault-template/` has ready-made templates if you want every note to look the same.

**Graph tips:** in Obsidian's graph view, use **Groups** to colour `path:Tickets`,
`path:Projects`, `path:Knowledge`. Filter `-path:Templates` to hide template dots.

---

## 🔴 Troubleshooting

| Problem | Fix |
|---|---|
| `/` commands don't show | Open each `.prompt.md`, change `agent: agent` to `mode: agent`, save, then **Ctrl+Shift+P > Developer: Reload Window** |
| Copilot ignores the skill | Check the file is named exactly `SKILL.md` in `.copilot/skills/second-brain/`, or use the one-project shortcut in Step 2 |
| Copilot asks where the vault is | Do Step 5, or check the path on the Vault location line (Step 3) |
| Copilot can't edit files | Make sure chat is in **Agent** mode, not Ask or Edit |
| No Claude model in the list | Your company may limit models; ask IT which are enabled |

---

## 🛡️ Safety rules built into the skill

```diff
+ Asks where the vault is before reading or writing; never guesses or creates one.
+ Every edit shows in chat with Keep or Undo.
- Never runs terminal commands or scripts. File tools only.
- Never deletes files. Asks before merging duplicate notes.
- Never writes passwords, tokens, keys or customer data.
```

---

## 🟠 The presentation

`presentation/second-brain-talk.html` is a 10-slide talk: human brain vs LLM brain,
why information is scattered, how the brain wires memories, how Obsidian copies that,
and the four commands. All images are inside the file.

To present: clone or pull the repo, double-click the file to open it in Chrome or Edge.
(github.com shows only the code.) Use the arrow keys or Space to move, and press **E**
to edit any text.
