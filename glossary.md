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

## Session 8 — Ship a useful agent (deploy on a schedule)

Turned the agent into a real product: `digest.py`, a morning brief that fetches AI + markets news, has Sonnet write it up, and delivers it two ways — a published web page and an email — then runs itself every morning on GitHub's servers with the laptop closed. Built as `digest.py` + `.github/workflows/digest.yml`.

**Shipping (the last mile)** — Making something *work* and making it *run itself, reliably, without you* are two different jobs. Session 8 is the second: delivery, secrets, and scheduling. The code was the easy part; getting it to run somewhere else, on its own, safely, is the deploy.

**Deployment** — Getting your code to run somewhere other than your own machine. "Works on my Mac" isn't shipped; "runs in the cloud when my laptop's asleep" is. The whole session is about crossing that gap.

**Environment variables** — Values the operating system hands a program when it starts, instead of the program reading them from a file. The move that lets *one* file run in two places: on your Mac `get_secret()` falls back to `key.txt`; in the cloud there is no `key.txt`, so the same code reads the value from the environment. `secrets.env` is the local convenience version (a gitignored `.env` file); GitHub Secrets is the cloud version.

**Secrets management** — Keeping credentials out of your code and out of git. What we did: real secrets live in gitignored files (`key.txt`, `secrets.env`) or an encrypted store (GitHub Secrets), never in the repo — and you give a program a *narrow, revocable* credential, never your master password.

**App password (Gmail)** — A single-purpose, revocable 16-character password you generate for one program, so your real Google password never touches the code. Requires 2-Step Verification. If it leaks you revoke just that one; your account is untouched. The principle is **least privilege**: hand out the smallest, most disposable credential that does the job.

**Token scopes (least privilege, cont'd)** — The same idea for GitHub tokens. Your Session-3 token could push code but *not* create workflow files, by design — GitHub guards workflow files specially because they run code — so we added the `workflow` scope. A scoped credential limits the blast radius of a leak: a feature, not a hassle.

**SMTP** — The internet's standard protocol for *sending* email. `digest.py` connects to Gmail's SMTP server over SSL, logs in with the app password, and sends the brief. Python's built-in `smtplib` does it in a few lines.

**Cron** — A scheduler that runs a job on a repeating time pattern. Five fields: `minute hour day month weekday`. GitHub runs cron in **UTC**, so our `0 23 * * *` (23:00 UTC) fires at 07:00 Singapore. Cron is how "do this every morning" becomes a concrete instruction.

**GitHub Actions (CI/CD, cont'd)** — GitHub's automation service: it runs jobs on its own machines, triggered by events. Session 4's Pages was CI/CD you *inherited* (a push auto-deploys); here you *authored* it. The pieces: a **workflow** (the `.yml` recipe of steps), a **runner** (the fresh Linux machine GitHub spins up per run — `runs-on: ubuntu-latest`), **triggers** (`schedule:` for the daily cron, `workflow_dispatch:` for the manual "Run workflow" button), and **permissions** (`contents: write`, so the job can commit the new `digest.html` back to the repo).

**YAML** — The indentation-based config format workflow files are written in (`key: value`, lists with `-`). Not code you run — a structured description the tool reads. Whitespace matters.

**"Works on my machine" (environment parity)** — The classic deploy bug, hit live: the code ran perfectly on your Mac but failed in the cloud with a 401, because the API-key *secret* in GitHub had a stray character. When something works locally but breaks when deployed, suspect the environment first — secrets, versions, network — not the code. Nine times out of ten it's a secret or config mismatch.

**Model choice as a cost/quality lever (cont'd)** — We write with **Sonnet** (sharper synthesis) rather than Haiku, accepting a few cents per run for a brief you'll actually read — a deliberate cost-vs-quality trade, ~$1/month once a day. Plus a **model fallback**: if Sonnet is unavailable the code drops to Haiku and keeps going, so a model outage never means no brief — the "degrade gracefully" instinct from Session 7, applied to the model itself.

**RSS feed** — A structured (XML) list of a site's latest items: title, link, short description. Cleaner and cheaper for a model to read than scraping a cluttered homepage. We read seven feeds across four providers (Google News, The Verge, Hacker News, CNBC) so **no single source is load-bearing** — if one fails some morning, the others still carry the brief (source diversity as a guardrail; on the first run one feed came back empty and the agent just flagged it and moved on).

## Session 9 — Build a discovery agent (the Scout)

Built scout.py — an AI-ecosystem SCOUT. Where the digest *summarised* what you pointed it at, the Scout *discovers*: given a thesis and the companies you already track (watchlist.json), it searches the live web, judges what fits, proposes new companies for your approval, and writes the ones you accept back into its own watchlist. First run found 10 real candidates (you kept 9), heavily Australian — Heidi Health, Lyrebird, Lorikeet, Neara, BrainChip, Q-CTRL, Appen, Andromeda Robotics, Groq.

**Monitor vs. Scout** — Two modes an agent can run in. A *monitor* watches a fixed list and reports what changed (the digest, essentially). A *scout* goes looking — it finds new things to add. Scout is the jump from "watch what I named" to "find what I'm missing," which for a BD/partnerships person is the more valuable half.

**Web search as a tool** — Until now the model only saw a URL you handed it (`fetch_url`). Here we switched on Anthropic's built-in `web_search` tool: inside a single API call, the model decides what to search, runs the searches itself, reads the results, and reasons over them. That's the leap from "read this page" to "go find out." It's a *server-side* tool — Anthropic runs the searches — unlike the client-side `fetch_url` you wrote by hand in Session 6. We biased results toward Australia with `user_location`.

**LLM-as-filter** — Using the model not to generate but to JUDGE: does this fit my thesis? is it already on my list? Pointing a model at messy results and asking it to sift is most of what real AI products actually do.

**Persistent state (read and write)** — The Scout reads watchlist.json to know what it already tracks, and writes your approved additions back into it. Your first agent that *changes its own data* and remembers across runs — the foundation under every assistant that seems to "learn" what you've told it.

**Human-in-the-loop** — The agent never adds anything itself; it proposes, you approve (a/s/q per candidate). That approval gate is the single most important safety pattern in agentic products: the model suggests, the human decides. It's also what keeps a discovery agent from quietly filling your list with noise.

**Config vs. engine** — The watchlist (*what* to track) is a data file; the Scout (*how* to track) is code. Keeping them separate means re-aiming the agent — new thesis, new names — never touches the engine. Good practice you'll see everywhere.

*(Next up — Monitor mode: watch the now-33-company list for real day-to-day changes, then deploy the whole tracker. Or RAG, MCP, a custom domain. See PLAN.md.)*

## Session 10 — Make the tracker self-running (scheduled Monitor + Scout)

Built ai-tracker/ — the Scout plus a new Monitor, run weekly by GitHub Actions in a PRIVATE repo, delivering one email: "What moved" (real news on tracked companies) + "New candidates" (awaiting your approval). tracker.py is the robot; approve.py is your half.

**Public vs. private repo** — Your website repo is public: anyone can read every file in it, not just the pages. The tracker's watchlist holds personal notes, so it got its own private repo. Rule of thumb: *where code runs* and *who can read it* are separate decisions — decide visibility on purpose, per repo.

**Batching** — Checking 33 companies in one giant call gives the model too much to juggle and makes one failure fatal. We check ~6 at a time. Smaller jobs = sharper focus, bounded cost per call, and a failed batch is just flagged ("Health check") while the rest still deliver.

**Delta / change detection** — A monitor's job is to report what *changed*, not everything it saw. Two layers: the prompt asks only for material news inside a 7-day window, and code then drops anything off-list, undated, out-of-window or without a source.

**De-duplication with memory (state)** — monitor_state.json remembers every story already sent you (keyed by its URL), so last week's news never reappears. Old entries expire after 90 days so the file doesn't grow forever.

**Asynchronous human-in-the-loop** — A scheduled job can't stop and ask "a/s/q?". So we SPLIT the steps: the robot *proposes* weekly (parks names in pending.json); you *approve* whenever you like (approve.py). Skips are remembered as "rejected" so they're never re-proposed. This propose/approve split is how most real agentic products handle human sign-off.

**State in two places (sync)** — The cloud run writes pending.json; your laptop writes watchlist.json. Same files, two copies — so approve.py PULLS from GitHub first and PUSHES after. Forgetting to sync = the two copies drift apart (a "merge conflict" when git can't reconcile them).

**pause_turn** — When the model does a lot of server-side searching, the API can return `stop_reason="pause_turn"` = "not finished, call me again". We pass its partial work back and let it continue — with a cap, as always.

**Wrapper (metering)** — We wrapped the API call once so *every* call — monitor and scout — adds its tokens and searches to a running cost meter. Each email ends with "Run cost ≈ $X". First real run: **$1.69** (~$7/month weekly) = 42 searches (~$0.42) + 389k input tokens (~$1.17) + 7k output (~$0.11). The searches are cheap; the *search results re-entering as input tokens* are 70% of the bill. Search-heavy agents are input-token-heavy — the levers are fewer searches per batch, or a cheaper model for the monitor.

**Loud failure (exit codes)** — A program ends with an exit code: 0 = success, anything else = failure. If the email doesn't send or most batches fail, tracker.py exits 1, so GitHub marks the run red *and emails you*. The direct lesson of the digest silently failing for weeks in October: a scheduled job must fail noisily. A "quiet week" email is also sent on purpose — silence should never be ambiguous.

**Dry run** — `python3 tracker.py --dry-run` does the whole job but sends nothing and saves nothing. Standard practice before letting automation act for real.

**Mocks (testing without spending)** — Before any real run we swapped in a fake Anthropic client that returned deliberately awkward answers — a "pause", old news, an off-list company, unparseable output, a crashed call — and checked each guardrail caught it. Free, fast, and repeatable; real runs then only test what mocks can't (the quality of the model's judgement).

**Source quality / grounding** — The first real run's weakest items all had one thing in common: the "source" was a homepage, blog index or listing page, not an article — and one of them (Kimi K3 "by Google" on *Amazon* Bedrock) was simply misattributed. A model citing a vague page is a classic sign it's stretching. Fix = two layers: the prompt demands the specific article with the company as the actor, and a cheap code check (`looks_like_article`: the URL must end in a long slug or an ID number) drops anything that doesn't. On that run it removed exactly the 6 weak items and kept the 11 solid ones. Lesson: *prompt for quality, then verify in code* — never rely on the prompt alone.

**Padding** — Models like to sound relevant: every "why it matters" ended "…across APAC markets". Told it explicitly to mention APAC only when the story genuinely involves it, and capped the line at 25 words.

**Second look (verify-then-keep)** — Dropping weak-sourced items lost real stories along with wrong ones. So instead of binning them, a "sub-editor" step runs ONE focused search per weak item: find the specific article, confirm it happened, confirm the right company did it. Confirmed → kept with the proper link; unconfirmed → dropped, and listed at the bottom of the email with the reason, so you can see what was filtered. Capped at 15 checks × 2 searches per run (raised from 8 after the real run used all 8 in half the batches; worst case ~+$0.75). This is a lightweight form of a well-known pattern: one model call *generates*, a second call *checks* (generator/verifier).

**Trust, but verify the verifier** — The checker's answer goes through the *same* code checks as the original. In testing, it "verified" a story but handed back a homepage — the code rejected it anyway. A model checking a model is better than nothing; a model checked by deterministic code is better still.

**Open web vs. curated sources** — The digest reads 7 fixed RSS feeds (curated: predictable, narrow). The tracker searches the whole web — the model writes its own queries every run (open: wider net, more junk). Open search is why the source checks matter. If junk sites keep recurring, the web_search tool also accepts `blocked_domains` (never use these sites) or `allowed_domains` (only these) — a dial between the two approaches.

**One rule, defined once** — The second dry run showed the sub-editor rejecting stories dated 1–2 days before the window, which the first check would have *accepted* (it had a 2-day grace; the sub-editor didn't). Two parts of the same system applying different rules = inconsistent results. Fix: define the window once (`EARLIEST`) and use it everywhere. Same run: "the company must be the actor" was too literal — it rejected Cognizant committing 25,000 staff to OpenAI. Loosened to "a principal party (actor, or named party to a deal)". Tuning guardrails is iterative: too loose lets junk in, too tight throws real news out — you only find the line by running it on real data.

**Prompts are requests, code is enforcement** — Told the Scout "no subsidiaries of companies I track"; it proposed Leonardo.Ai ("now acquired by Canva") anyway, twice. So a code check now drops any candidate whose description says acquired/owned/part-of AND names a tracked company. Pattern seen all session: anything that *must* hold goes in code; the prompt just makes violations rarer.

**Run-to-run variance (non-determinism)** — Two runs over the same week gave different lists: the NEXTDC AU$715M stake bid appeared in run 1 and not run 2. Each run is a *sample* — the model picks different searches and different results. Mitigations: the weekly cadence plus the 2-day grace give stories more than one chance to be caught; more searches per batch would help but cost more. Worth knowing before you trust any single AI-generated report as complete: good at "here's what moved", not a guarantee of "nothing else did".

Quality across the three dry runs: run 1 = 17 items, 6 weak or wrong sources; run 3 (with source check + sub-editor) = 16 items, all linked to a specific article (OpenAI's own site, Bloomberg, GlobeNewswire, Databricks' blog), "why it matters" lines specific instead of generic. Cost rose $1.69 → $2.03 (~$8–9/month). That's the quality/cost trade made on purpose.

**Key rotation** — Replacing a secret that may have been exposed: make a new key, update every place that uses it (key.txt locally + the secret in each GitHub repo), TEST it works (local script, then one cloud run), and only then delete the old key. Order matters — delete first and everything breaks until you finish. Done 6 Nov after a key appeared in a screenshot.

**Scheduled jobs run late on the hour** — GitHub's scheduler is overloaded at :00 because everyone picks round times; our "7am" brief was actually arriving at 10–11am. Fix: pick an odd minute (06:47). A general lesson — shared infrastructure gets congested at the obvious times.

---

## Session 12 — A real web app (Early Signals)

**Frontend vs backend** — The *frontend* is what runs in the browser: the HTML page, its styling (CSS), the form you type into. The *backend* is the program on the server (here: app.py on your laptop) that receives requests, applies the rules, stores data and sends pages back. Rule of thumb: the frontend is for convenience, the backend is where the truth and the rules live.

**HTTP (request / response)** — The language browsers and servers speak. Every click is a *request* (a method + a path, e.g. `GET /p/tim`), and every answer is a *response* (a status code + content, usually HTML or JSON). Each request stands alone — the server doesn't "remember" you between clicks unless something is added to make it (that's *sessions*, Session 14).

**GET vs POST** — The two methods you'll see most. GET = "show me something" (safe to repeat; it's what typing a URL does). POST = "here is some data, do something with it" (submitting a form). A form with `method="post"` sends its fields to the backend in the body of the request.

**Status codes** — The three-digit number on every response. 200 = OK. 302 = "go over there instead" (a redirect). 400 = "your request was bad" (e.g. the form failed validation). 404 = "no such page". 500 = "the server broke". Monitoring in Session 17 is largely counting these.

**Route** — A rule mapping a method + URL path to a function in the backend. `@app.route("/p/<slug>")` means "when someone asks for /p/anything, run this function with slug = anything". A web app is mostly a list of routes.

**Web framework (Flask)** — A library that handles the plumbing of HTTP — listening on a port, parsing requests, routing, templates — so you only write the parts specific to your product. Flask is small and Python; Django (Python), Rails (Ruby), Express/Next.js (JavaScript) are the other common choices. The concepts carry across all of them.

**Template** — An HTML file with blanks that the backend fills in for each request (marked with double curly brackets, e.g. a blank for the user's name, or a loop that repeats a line for each hunt). Flask's template language is Jinja. Templates *escape* what they insert by default, so if a user types `<script>` into a field it is shown as text, not run — this blocks a whole class of attacks (XSS, cross-site scripting).

**Form validation — "never trust the browser"** — The HTML has `required` on some fields, which stops honest users submitting a blank form. But anyone can send a raw HTTP request that never touches your page. So every rule is re-checked in the backend (`validate()`); if anything fails, the form comes back with a 400, the errors highlighted and the answers still filled in, so nothing typed is lost.

**POST → redirect → GET** — After a successful save, the backend doesn't return a page directly; it replies "302, go to /p/tim". The browser then does a normal GET. Result: pressing refresh just reloads the profile instead of re-submitting the form (the "Confirm form resubmission?" problem). Standard practice on every serious site.

**API (the same data without the HTML)** — `/p/tim` returns a page for humans; `/p/tim.json` returns the same profile as JSON for programs. That second kind of endpoint is an API. Most products are an API first, with the website as just one of its clients (alongside phone apps, partner integrations — and AI agents).

**Config generated, not hand-written** — The form's real job is to produce the same profile.json the Radar engine already reads. The engine didn't change at all — the test proves radar.py's own prompt and filters run on the form's output. This is the config-vs-engine separation from Session 9 paying off: because the engine reads config, you can put any interface in front of it (a form today, a chat or an admin console later).

**Templates per user (one engine, many users)** — The signal hunts are written once as templates — "{sectors} companies entering {where}" — and filled with each user's answers. That's how one engine can serve a thousand users without anyone writing a thousand prompts. It's the first real step to *multi-tenancy* (Session 15).

**Slug + path safety** — A slug is the URL-friendly version of a name ("Tim Brown!" → `tim-brown`). Here it's also the filename, so it's restricted to a–z, 0–9 and "-": otherwise someone could request `/p/../../secrets` and read files outside the app's folder (*path traversal*). Lesson: anything from a user that touches a filename, a database query or a shell command must be cleaned first.

**Debug mode / localhost** — `app.run(debug=True)` reloads on every save and shows errors in the browser — great on a laptop, dangerous in public (it can expose your code). `127.0.0.1:5050` means "only this machine, port 5050": nobody else on the network can reach it yet. Going public properly is Session 15.

**Boardroom layer** — (1) The AI is a small part of an AI product: today was 100% "the layer around it" and that's typical — the interface, rules, storage and security are most of the build. (2) A form beats a config file because it *constrains*: users can only pick valid options, so the engine gets clean input and support costs fall. (3) An API-first design is what lets partners and agents integrate — a commercial asset, not just plumbing. (4) Today's storage (one file per user) breaks with two people saving at once and can't answer "which users want Singapore?" — that's exactly why Session 13 brings in a database.
