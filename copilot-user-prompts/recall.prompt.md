---
agent: agent
description: Brief me from my second brain on a ticket, project or topic
argument-hint: PROJ-1234, a project name, or a topic
---
Use the **second-brain** skill in **Recall** mode. Follow its ground rules: know the vault
folder first (ask me if unsure), and do not run any commands.

Topic: ${input:topic:Jira key, project or topic}

Read the matching note, follow its links one level out and read the last 3 daily entries
that mention it. Give me a short briefing: status, what was done, open questions, steps
that worked, relevant docs, all as [[links]].
