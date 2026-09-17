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

## Session 4 — Deploy (GitHub Pages)

**GitHub Pages** — GitHub's free web hosting for static sites (HTML/CSS/JS). Flip one setting and the repo's files are served at a public URL. For a repo named `username.github.io`, that URL is `https://username.github.io`. Ours went live at https://iamtimbrown.github.io with no code changes — the files were already pushed.

**Going live / production URL** — Moving from `localhost` (reachable only on your machine, only while your local server runs) to a public address on an always-on machine anyone can reach. The code doesn't change — where it runs and who can reach it does. That's the essence of "deploy."

**Environment** — A named place where a copy of the project runs. **Local / development** = your laptop, where you edit and break things safely. **Production ("prod")** = the real copy users hit. Many teams add **staging** in between: a production-like copy for final testing before customers see a change. Keeping them separate limits blast radius — make mistakes in dev, catch them in staging, never in prod. "Did this go to prod?" is asking which environment a change reached.

**CI/CD (continuous integration / continuous deployment)** — An automated pipeline from "code merged" to "live in production." We used one without noticing: `git push` to `main` caused GitHub to automatically build and publish the site — no manual file uploads. Modern teams deploy this way constantly. Commercially, deployment frequency and pipeline safety are proxies for how fast a company can ship and respond.

---

## Session 5 — Call Claude from code (the AI layer begins)

**API key** — A scoped, expiring, revocable credential that authenticates your code to a provider's API. Same least-privilege idea as the GitHub PAT (Session 3). Cardinal rule: never put it in your code, or a `git push` would publish it. We kept ours in `key.txt`, listed in `.gitignore` so git ignores it — the standard "secrets live in a gitignored file" pattern.

**SDK (software development kit)** — A ready-made library that hides the low-level plumbing of talking to an API. We installed the `anthropic` SDK with `pip3 install anthropic`; it turns "make an authenticated HTTPS request with the right headers and JSON" into one line: `client.messages.create(...)`.

**API (met it)** — A way for one program to use another over the internet, machine-to-machine. Our Python script called Anthropic's API, a model generated a reply, and it came back. Every AI product is built on this exact mechanism. Commercially: API usage is metered, which drives AI cost structures.

**Token** — The unit AI models read and write text in (~¾ of a word). Our first call used 25 input tokens + 78 output tokens. Providers charge a price *per input token* and a higher price *per output token*, so tokens are the atomic unit of AI COGS: tokens in + tokens out × a per-model price = the cost of a call.

**AI COGS scale with usage** — Unlike traditional software (near-zero marginal cost per extra user), every AI call burns tokens that cost money. Cost scales roughly linearly with adoption, which is why AI businesses obsess over cost-per-query and why gross margin is a live question, not a given.

**Model choice as a cost lever** — Cheaper/faster models (Haiku) vs. most-capable/pricier ones (Opus) can differ many-fold in per-token price. Routing easy tasks to cheap models and hard ones to expensive models is real engineering that maps straight to the P&L.

**Context window** — The maximum number of tokens a model can consider at once. Caps how much background (documents, history, data) you can feed per call. "200K vs 1M context" comparisons are about this — bigger windows do more per call, but you pay for every token you put in.

---

## Session 6 — Build an agent (tool use)

**Agent** — An AI program that doesn't just answer, but takes actions: it calls tools, reads the results, and loops until a task is done. In `agent.py` we gave the model a goal ("compare my live site to my local file") and two tools, and it decided on its own to fetch the page, read the file, then compare. We never scripted the steps — that autonomy is what makes it an *agent* rather than a script.

**Tool** — Just a normal function *we* wrote (e.g. `read_file`, `fetch_url`). The model can never run code itself; it can only *ask* us to run a tool by name. Our code runs it and hands back the result. We stay in control of what actually happens.

**Tool use / function calling** — The mechanism that lets a model trigger those functions. We describe each tool to the model (name + a plain-English *description* + what arguments it takes); the model uses the description to decide *when* to reach for it. Writing good tool descriptions is half the job of building a reliable agent.

**The agent loop** — The engine of every agent. We keep the whole conversation in a `messages` list and call the model repeatedly: if it asks for a tool we run it, add the result to the conversation, and call again; if it gives a final answer we stop. Mechanically, "agentic AI" is just this loop — model → tool → result → model, until done. Demystified, there's no magic in it.

**`stop_reason`** — The field on each API reply that says *why* the model stopped this turn. `"tool_use"` = it wants a tool run before it continues; `"end_turn"` = it's finished and gave a final answer. Our loop branches on exactly this.

**`tool_use` / `tool_result`** — The two message pieces that carry the loop. The model emits a `tool_use` block (which tool, which arguments, plus an `id`); we run it and send back a `tool_result` block tagged with that same `id` so the model knows which answer goes with which request.

**Boardroom layer — demo vs. product; reliability is the hard part** — An agent that works once in a demo is easy; one that works *every* time on messy real-world inputs is the entire challenge. A model can call the wrong tool, pass bad arguments, or loop forever. Production agents wrap this loop in guardrails: step limits, error handling, permissions on what each tool may do, and **evals** (systematic tests). Commercially, the gap between "cool demo" and "shippable product" is almost entirely reliability engineering — and it's where most of the real cost and time goes.

**Boardroom layer — agents multiply token cost** — Each turn of the loop is a *separate* metered API call (Session 5), and every tool result gets fed back in as input tokens on the next call. A task that takes five tool-steps costs roughly five calls' worth of tokens, and long tool outputs (a fetched web page) inflate every subsequent call. Agents are powerful *and* the reason AI bills can balloon — which is why step limits, output trimming, and cheap-model routing (Haiku here) are cost levers, not just tidiness.

*(evals, MCP — defined when we meet them. RAG and fine-tuning are now defined below.)*

---

## Side topic — AI/ML infrastructure economics
*(Came up via a role description, not a build session. The felt version — renting vs. owning GPUs — is pencilled in for a later session.)*

**Inference vs. training** — The two things you can do with a model. **Training** is the one-time, massively expensive job of *building* a model — feeding it data until it learns. **Inference** is *using* the finished model to get an answer. Every call we've made (Session 5's hello-world, Session 6's agent) is an inference — we've never trained anything. This distinction is the hinge for the whole topic: "inferencing costs," "GPU capacity," and "deployment architecture" are all about *running* models, not building them.

**Inference cost** — What it costs to run one model call: tokens in + tokens out × a per-model price (Session 5). We've watched this on the meter and felt the levers (Haiku vs. Opus; the agent finishing in 2 calls not 3). "Our inferencing costs are killing our margins" means the thing we've watched tick up: an AI product's cost-of-goods scales with every query, unlike normal software.

**GPU** — The specialised chip (e.g. NVIDIA H100) that models actually run on. When we call the API, our prompt runs on GPUs in Anthropic's data center; we never see them because that's the whole point of buying inference as an API — someone else owns the hardware.

**GPU capacity** — The layer beneath our API call, deliberately hidden by it. GPUs are scarce and expensive, and they're the binding constraint on how many users you can serve at once — an idle GPU is money burning. Bigger context windows need more GPU memory per request (why long-context calls cost more). Rate limits are capacity management reaching us through the abstraction.

**Model deployment architecture** — *Where* a model lives and *how* you serve it. We've already used the most common pattern without naming it: **calling a hosted API** from a frontier provider — zero infrastructure, pay per token, someone else owns the GPUs and the uptime. The main alternative is **self-hosting** an open-weight model (e.g. Llama) on GPUs you rent or buy — more control, privacy, and possibly lower cost at high volume, but now you own the capacity, ops, and reliability. In between sit the real levers: routing easy queries to cheap models, caching repeated prompts, batching requests to keep GPUs full.

**Build vs. buy (infrastructure)** — The boardroom decision behind deployment architecture. **Buy** = call a hosted API: fast, lean, no infra to run. **Build** = self-host on your own/rented GPUs: worth it when scale, data privacy, or gross margin justify taking on the infrastructure and its risk. Most companies start by buying and only build when the volume math or a privacy requirement forces it. We are firmly on the "buy" side today.

---

## Side topic — Fitting a model to a use case (RAG vs. fine-tuning)
*(Came up asking whether "training for a use case" affects inference cost/speed. Key insight: only one of these two is actually training, and they hit cost in opposite directions.)*

**Fine-tuning** — Actually *training*: you adjust a model's weights on your own examples so it internalises your task, style, or format. Payoff for inference — a fine-tuned *small* model can match a big general model on a narrow task, so you get to run the cheap, fast model and send shorter prompts (the knowledge is baked in, so fewer instructions/examples per call). Both cut inference cost and latency. The catch: the fine-tuning job itself costs money upfront, so it pays off at scale. Best for style/format, narrow-task skill, or shrinking the model you need.

**RAG (retrieval-augmented generation)** — *Not* training, and often confused with it. Instead of baking knowledge into the model, you *fetch* relevant documents at query time and stuff them into the prompt as context. Effect on inference: usually *increases* per-call cost (retrieved text = more input tokens) and adds a little latency for the lookup step. You use it anyway because it buys **accuracy and freshness** — a general model can answer about your *private* or *up-to-the-minute* data with no retraining. RAG buys correctness, not cheapness.

**RAG vs. fine-tuning (the decision)** — Not rivals so much as different tools. **RAG** for knowledge that is large, private, or changes often (facts, documents, current data). **Fine-tuning** for behaviour: style, format, a narrow skill, or dropping to a smaller/cheaper model. Real systems often do both — fine-tune the behaviour, RAG the facts.

**Fit lowers cost at the workflow level too** — Even when a technique doesn't cut the *per-call* price, better fit means fewer calls: fewer retries, less back-and-forth, shorter agent loops. We saw a hint of it in Session 6 — the agent got it right and finished in 2 calls, not 3. At scale, "right the first time" is real money.

---

## Side topic — Self-hosting, and open vs. closed models
*(Came up drilling into what "run your own model" actually means in practice.)*

**Same as cloud vs. on-prem** — Build-vs-buy for AI is the familiar cloud-vs-on-prem decision moved up a layer, and it's really three tiers: **own GPUs in your own data center** (= on-prem), **rent GPUs and run your own model** (= IaaS / cloud), **call a hosted API** (= SaaS / managed). The old tradeoffs carry straight across: capex vs. opex, control/data-residency vs. speed/convenience, and utilisation economics (an idle owned GPU is wasted capital, pay-per-use is elastic). Two AI-specific twists: (1) high-end GPUs are *scarce and less elastic* to rent than commodity CPUs (allocation-gated, export-controlled); (2) the "buy" option hands you a **frontier model you could never build yourself**, so the "build" side has a *capability ceiling* the old on-prem story never had.

**"Run your own" ≠ own data center** — Realistically, self-hosting means *renting dedicated GPU capacity in someone else's building*, not pouring concrete. The ladder, lightest to heaviest: **managed open-model service** (Bedrock, Vertex, Together, Fireworks — they serve an open model you chose) → **rented dedicated GPU instances** (rent H100s from AWS/GCP/Azure/CoreWeave/Lambda, deploy the model, run the serving yourself) → **reserved/committed capacity** (same, but a 1–3yr commitment for better price + guaranteed availability). Owning an actual **data center** is only for hyperscalers, frontier labs, and a few mega-scale players — because a data center is its own business (multi-year build, security, and above all **power and cooling**, which for power-hungry GPUs is now the real bottleneck).

**A rented GPU arrives empty** — It's bare compute: GPUs, OS, drivers, nothing else. Whatever model runs on it, *you* put there. So instances are never "pre-loaded" with anyone's model — and crucially, you **cannot** load a closed frontier model (GPT, Claude, Gemini) onto your own hardware at all. Self-hosting therefore always means running an *open* model.

**Open-weight vs. closed model** — The dividing line. **Open-weight** models (Llama, Mistral, Qwen, DeepSeek, Gemma) publish their **weights** — the billions of learned parameters that *are* the trained model — for download; you can run and fine-tune them on your own GPUs. **Closed / proprietary** models (GPT, Claude, Gemini) never release their weights; they live inside the provider's systems and are reachable **only via the provider's API** (or a partner-managed deployment). Quick test for any setup: *can they hand you the weights?* Yes → open-weight, truly self-hostable. No → you're buying managed access, however "dedicated" it sounds.

**Weights** — What a model actually *is*: a giant list of numbers. A neural network is built from artificial "neurons," and each one multiplies its inputs by numbers and adds them up. Those multiplier numbers are the weights — think of each as a **knob** (like a slider on an audio mixing desk) whose setting shapes the output. A model is billions of these knobs wired in layers; **training** is the automatic process (gradient descent) of setting every knob to the value that makes outputs come out right, after which they're frozen — and that frozen set of numbers *is* the model. Running it (inference) is just pushing your input through all that fixed arithmetic. (Two caveats on the knob picture: no human turns them — there are far too many — and no single knob has a clean label like "volume"; meaning is smeared across millions of interacting knobs.)

- *Tiny example:* a house-price model `price = (w1 × sqft) + (w2 × bedrooms) + b`. Training might set `w1 = 150`, `w2 = 10,000`, `b = 50,000`. Those three numbers *are* the model. An LLM is the same idea with billions of weights over hundreds of layers.
- *Scale:* "an 8B model" = **8 billion weights**. Each is stored as a small number (~2 bytes), so an 8B model is roughly a **16 GB file**; a 70B model ~140 GB. That file is the whole asset.
- *Formal word:* a weight is a **parameter**; adjusting them is **tuning** / **fine-tuning** — the vocabulary is the knob metaphor made literal.

**Open-weight, made concrete** — **Llama 3.1 8B** is open-weight: Meta published that ~16 GB file of numbers, so you can download it (e.g. from Hugging Face) and run it on your own GPU. **Claude / GPT** are closed: no such file exists to download at any price — you only reach them through the API. The single test for "open-weight vs. closed" is *does a downloadable file of the weights exist?*

**Getting a frontier model on dedicated infra** — Possible, but it's a *managed-access* commercial package, not the weights. Claude via Amazon Bedrock / Google Vertex; GPT via Azure OpenAI — the provider runs the model inside a cloud environment, often with dedicated/reserved capacity (**provisioned throughput**), data isolation, and compliance guarantees. You call it privately; you still never see or control the model files. It's the "buy" side wearing a private room, and a separate purchase from renting bare GPUs.

**Open-weight ≠ open source** — A precision point vendors blur. **Open-weight** = you can download the weights. **Open source** (strict sense) would also mean the *training code and data* are released so you could rebuild the model from scratch — which almost no popular "open" model actually does (Llama ships weights under Meta's *community license*, data withheld, with usage restrictions and a >700M-user carve-out). So ask two separate questions of any "open" model: *(1) can I get the weights?* (open-weight or not) and *(2) what does the license allow commercially?* (Apache-2.0 permissive vs. a restricted community license). "Open" tells you about the first, not the second — the license is where diligence lives.

**When does self-hosting make sense?** — Since self-hosting means an *open* model (never a closed frontier one), it's tempting to assume it's only for narrow, fine-tuned use cases. That's one driver, but there are five, and the narrow-task one is rarely the heaviest:
1. **Regulation / data control** — the data legally can't leave (healthcare, defense, finance, government, data-residency/sovereignty rules). Often a *general-purpose* open model — the driver is control, not specificity. This is the one that shows up most in serious enterprise deals.
2. **Cost at scale** — huge, steady, predictable volume where owning the serving stack beats metered API per-token pricing. Flips purely on volume, task breadth aside.
3. **Latency / edge / offline** — must run on-device, offline, or with no network round-trip (factory floor, vehicle, phone).
4. **Lock-in avoidance** — own your model version so a provider can't deprecate it or reprice under you.
5. **Narrow task, fine-tuned** — a small open model tuned to one well-defined job (ticket classification, invoice extraction) can match or beat a general frontier model, cheaper and controllable. The intuitive case, and real — just not the only one.

Two caveats: self-hosting doesn't *require* fine-tuning (many just prompt or RAG an open model), and the "open models are only good for narrow tasks" assumption is dating fast — the best open models (Llama, DeepSeek, Qwen) are now strong enough to self-host as fairly *general* assistants. Good follow-up when you hear "we run our own models": *which of these five is driving it?* — the answer reveals their real constraints.

---

## Side topic — The infrastructure stack: providers, sovereignty, neoclouds, colocation
*(Came up mapping the role phrase "GPU capacity, inferencing costs, model deployment architectures" all the way down to who owns the buildings. See the companion diagram: `ai-infrastructure-stack.html`.)*

**Who you buy compute from (self-hosting)** — Tiers: **hyperscalers** (AWS, Azure, GCP) rent GPU instances + managed services, the default; **GPU-specialist clouds / "neoclouds"** (CoreWeave, Lambda, Nebius, Crusoe, Nscale) are purpose-built GPU alternatives, often cheaper/more available; the **chip layer** (NVIDIA GPUs + DGX, AMD, Google TPUs, AWS Trainium); **OEM hardware** for truly-owned kit (Dell, HPE, Supermicro, Lenovo); and **serving software** (vLLM, NVIDIA NIM/Triton, HF TGI) as the plumbing. For most companies, "self-host" = rent from a hyperscaler or neocloud, not build.

**Sovereign cloud (a spectrum, not a binary)** — All three hyperscalers offer it, ranging: (1) **public cloud kept in-region** with contractual/technical controls (Microsoft *Cloud for Sovereignty* began here); (2) **partner-operated "trusted" clouds** where a *local* company runs it (Microsoft's **Bleu** in France w/ Capgemini+Orange, **Delos Cloud** in Germany w/ SAP; Google's **S3NS** in France w/ Thales); (3) **fully separate / air-gapped clouds** — AWS **European Sovereign Cloud** (launched Jan 2026, Brandenburg DE, EU-resident staff only, runs even if cut off) and Google **Distributed Cloud** (can run air-gapped). Plus independent EU providers (OVHcloud, Scaleway, T-Systems) and "sovereign AI" GPU clouds. Diligence questions: *who operates it? where do the data + keys live? can it run cut off?* Trade-off: more sovereign/isolated = fewer bleeding-edge services + higher cost.

**Neocloud** — A GPU-first cloud built as an alternative to the hyperscalers. Key facts: they **own their GPUs** (buy direct from NVIDIA) — they are *not* reselling hyperscaler capacity; the flow often runs the other way (hyperscalers rent GPUs *from* neoclouds, e.g. Microsoft ↔ CoreWeave). They own the *chips* but usually **rent the building** (colocation), not pour concrete. Brutally **capital-intensive**: funded by VC + **debt collateralised by the GPUs themselves** (CoreWeave debt reported ~$35B) + anchor customer contracts. Watch the **circular financing**: NVIDIA invests in neoclouds → they buy NVIDIA GPUs → NVIDIA/labs commit to rent from them. Risk lens: a leveraged bet on sustained demand *and* on GPUs (a melting, fast-depreciating asset) holding value; winner = best **capital efficiency** (keeping the chips utilised), not most GPUs.

**Colocation ("colo") & the data-center layer** — The buildings neoclouds and hyperscalers put GPUs in are owned/run by **specialist data-center operators** (Equinix, Digital Realty, QTS, Vantage, CyrusOne, Iron Mountain) — the "landlords," who lease space + power. They are **not** the hyperscalers: hyperscalers mostly build their own DCs *and* are big **tenants** of these same operators (tenant alongside the neocloud, not landlord above it). Underneath, the operators are largely owned by **infrastructure / private-equity capital** (e.g. Blackstone owns QTS) — so the DC layer is fundamentally a **real-estate play**. The binding constraint through the whole stack is **power** (power-ready land + grid + cooling for dense GPU racks) — whoever controls secured power holds the leverage.

**The stack, top to bottom** — Your app/agent → model access (buy API ↔ build/self-host) → model (open-weight ↔ closed) → compute provider (hyperscaler / neocloud) → GPUs (NVIDIA) → data-center building (colo operator, owned by PE) → **power & grid (the constraint)**.

---

## Session 7 — Make the agent reliable (guardrails + evals)

Took `agent.py` (the Session 6 demo) and hardened it into `agent2.py` — same loop, but built so it can't run away or crash, given a real task with a deliberately broken source, and checked automatically at the end.

**Demo vs. product** — An agent that works *once*, on a clean input, is a demo; one that works *every* time, on messy inputs, is a product. The gap between them is almost entirely reliability engineering — and it's where most of the cost and time in a real AI build goes. Session 7 is that gap in miniature.

**Guardrail** — A limit you put *around* the model because you don't fully trust it. The model is capable but not guaranteed; guardrails contain what happens when it misbehaves. Three we added: a step limit, tool error handling, and output trimming.

**Step limit (circuit breaker)** — A hard ceiling on how many times the loop may call the model (`while step < MAX_STEPS`). The demo used `while True` and trusted the model to stop; production never does, because a confused model can loop forever and *every loop is a paid API call*. The limit stops a runaway before it burns money — the single most important agent guardrail.

**Graceful degradation / error handling** — A tool must never crash the whole agent. Instead of letting an exception kill the program, the tool catches it and *returns* an `ERROR: ...` string, which is fed back to the model as that tool's result. The model then *sees* the failure and can recover — skip that source, retry, or report it honestly — instead of the whole run dying. We proved it by handing the agent one broken URL among three: it summarised the two that worked and flagged the one that didn't.

**Token discipline as a guardrail** — Trimming a fetched page to 4,000 chars before feeding it back isn't just tidiness: every character returned becomes input tokens on the *next* call (Session 5/6). Output trimming, step limits, and cheap-model routing are the levers that keep an agent's cost bounded.

**Evals (evaluations)** — Automatic tests for an AI system. You eyeball a demo once; you *eval* a product the same way every time, so you notice the day it breaks. Our first eval ran three concrete checks on the agent's output (finished within the step limit? produced an answer? correctly flagged the unreachable source?) and scored them PASS/FAIL. Real eval suites run dozens–hundreds of cases and track the score over time. **Evals are what let you say "reliable" with a number instead of a vibe** — and commercially, they're what gate shipping.

**LLM-as-judge** — The scalable version of an eval check. Simple checks use keyword/rule matching (crude, brittle); LLM-as-judge instead asks a *model* to grade the output against a written rubric. More flexible for judging things like "is this summary accurate and well-written," which keywords can't capture. Same idea as our eval, just a smarter grader.

*(MCP, RAG-in-practice, deployment/hosting an agent — for Session 8 and beyond.)*

