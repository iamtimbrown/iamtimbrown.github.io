# Tim's Tech & AI Glossary

Plain-English definitions, in roughly the order we met them. Updated each session.

---

## Session 1 — Running a website locally

**Terminal / command line** — The text-based way to control your computer. You type commands instead of clicking. Engineers live here because it's faster and scriptable.

**Command** — An instruction typed into Terminal, e.g. `cd`, `pwd`, `mkdir`.

**Directory** — Just the technical word for a folder. `cd` = "change directory" (move into a folder). `pwd` = "print working directory" (show where I am). `mkdir` = "make directory" (create a folder).

**HTML** — The language web page *content* is written in. Headings, paragraphs, links — all defined with tags like `<h1>` and `<a>`.

**CSS** — The language for how a page *looks*: colors, fonts, spacing. Lives alongside or inside the HTML.

**Server** — A program (and by extension, the machine running it) that waits for requests and responds — e.g. a web server sends back web pages. A "server" in a data center is just a computer that's always on, running server programs.

**localhost** — An address meaning "this machine." `localhost:8000` = "talk to the server running on my own computer." Not reachable by anyone else.

**Port** — A numbered channel on a machine that a server listens on (the `:8000` part). One machine can run many servers, each on a different port. Websites use port 443 (https) by default so you never see it.

**Deploy / ship** — To put software onto a server so it runs live for real users, rather than just on a developer's laptop. "When does it deploy?" = "when is it live?"

---

## Session 2 — Git

**Git** — A tool that tracks every change ever made to a project's files. The universal standard for managing code.

**Repo (repository)** — A project folder being tracked by git, including its full change history. "It's in the repo" = "the code officially exists in our shared project."

**`git init`** — Run once per project to start tracking it. Creates a hidden `.git` folder where all history is stored — turns a pile of files into a repo.

**Commit** — One saved snapshot of the project, with a note about what changed. Projects accumulate thousands of commits; they're the project's paper trail. Each gets a unique ID (a hash like `4868161`).

**Staging (`git add`)** — The step before committing: choosing which changes go into the next snapshot. Like putting files in a box before sealing it. `git add .` stages everything. The two-step stage-then-commit lets you snapshot some changes but not others.

**`git status`** — Shows what's changed since your last commit: untracked files (git isn't watching them yet) and modified files (changed since last snapshot).

**`git diff`** — Shows the exact lines that changed — removed lines marked `-`, added lines marked `+`. How you review a change before committing it.

**`git log`** — The timeline of commits, newest first. `--oneline` gives the short version.

**Branch / `main`** — A line of development. `main` is the default one. Teams create separate branches to work on features without disturbing `main`, then merge them back.

**HEAD** — A pointer to where you currently are in the history (usually the latest commit on your branch).

**Push / pull** — Push = send your commits to the online copy (e.g. GitHub). Pull = fetch others' commits down to your machine. This is how teams stay in sync.

**GitHub** — The dominant website for hosting repos online. Backup, collaboration, and increasingly the hub where code review and deployment kick off.

---

## Session 3 — GitHub

**Remote** — An online copy of your repo that your local repo is linked to. You push commits up to it and pull commits down from it. A repo can have several, but usually just one.

**`origin`** — The standard nickname for your main remote (your GitHub repo). Set once with `git remote add origin <url>`; after that you just refer to `origin`. Nothing special about the word — it's convention.

**`git push` / tracking** — Sends your local commits up to the remote. The first push used `git push -u origin main`: `-u` links local `main` to `origin/main` so future pushes are just `git push`. "Tracking" = that permanent link between your branch and its online twin.

**Personal access token (PAT)** — A long generated string that acts as a password for git operations. GitHub stopped accepting account passwords in 2021. A token is scoped (we used `repo`) and expiring (90 days) and revocable — so a leak is contained. This is the same least-privilege idea as API keys everywhere in software.

**Source of truth** — The one canonical copy of a project that everyone trusts and syncs to (your GitHub repo). "It's merged to main on GitHub" = it officially exists. The reference point for backups, code review, and deployment.

**`username.github.io`** — GitHub's magic repo name: a repo named exactly this becomes a free live website at that same address (via GitHub Pages). Ours is `iamtimbrown.github.io` — set up for Session 4.

---

## Coming up — the AI layer

**API** — A way for one program to use another program over the internet, machine-to-machine. AI products call a model provider's API. Commercially: API usage is metered, which drives AI cost structures.

**Token** — The unit AI models read and write text in (~¾ of a word). API pricing is per token, so tokens are the unit of AI COGS.

**Context window** — The maximum amount of text a model can consider at once. Limits how much background an AI can "hold in mind"; a key spec when comparing models.

**Agent** — An AI program that doesn't just answer, but takes actions: calling tools, checking results, looping until a task is done.

**Tool use / function calling** — The mechanism that lets a model trigger real actions (search the web, send an email) via functions a developer wrote. The building block of agents.

*(RAG, fine-tuning, evals, MCP — defined when we meet them.)*
