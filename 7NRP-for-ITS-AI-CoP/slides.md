---
theme: default
layout: default
title: The National Research Platform - Native v2
class: nrp-v2
transition: fade
canvasWidth: 980
aspectRatio: 16/9
favicon: false
fonts:
  sans: Arial
---

<V2Frame dark :footer="false" bodyClass="v2-cover">

<p class="v2-cover-kicker">THE NATIONAL RESEARCH PLATFORM</p>

# Insights from the 7NRP Conference, and implications for Cal Poly

<p class="v2-cover-meta"><strong>Brian Spolarich</strong> · AVP/CTO · ITS AI Community of Practice · May 2026</p>

</V2Frame>

<!--
Welcome. I'm going to spend the next twenty minutes giving you a tour of the National Research Platform — or NRP — and what I learned at the 7NRP conference earlier this month in San Diego.

My goal is to leave you with three things: a clear mental model of what NRP is and how it works, a feel for who is already using it and how, and a sense of why I think this matters for Cal Poly and for the work many of you do in IT.

This is intentionally a high-level talk. I'm not going to go deep on Kubernetes or networking — but I will point to where to learn more. Hold questions to the end if you can; if not, jump in.
-->

---


<V2Frame kicker="AGENDA" title="What we'll cover" page="2 / 23">

<div class="v2-agenda">
  <div><b>01</b><strong>What NRP is</strong><span>Vision, scale, and the headline numbers</span></div>
  <div><b>02</b><strong>How it works</strong><span>Kubernetes, Jupyter, GPUs, and the network underneath</span></div>
  <div><b>03</b><strong>Who uses it</strong><span>Researchers, instructors, students, and the LLM service</span></div>
  <div><b>04</b><strong>Where Cal Poly fits</strong><span>Current usage, sister CSU models, and campus on-ramp</span></div>
  <div><b>05</b><strong>The broader landscape</strong><span>ACCESS, NAIRR, NERSC, NDP, and what changes next</span></div>
  <div><b>06</b><strong>Takeaways</strong><span>Questions for ITS and the AI Community of Practice</span></div>
</div>

</V2Frame>

<!--
Six sections. We'll spend the most time in the middle three — how NRP works, who's using it, and what Cal Poly and the CSUs are doing today.

I'm aiming to leave four or five minutes at the end for discussion. If something I say sparks a thought, jot it down — we'll come back to it.
-->

---


<V2Frame kicker="WHAT IS NRP" title="Community-owned cyberinfrastructure" page="3 / 23">

<div class="v2-split v2-quote-slide">
  <div class="v2-quote">
    <p>"A global-scale Kubernetes cluster for research, education, and public-private partnerships — built and run by the community it serves."</p>
    <small>Frank Würthwein · San Diego Supercomputer Center</small>
  </div>
  <div class="v2-stack">
    <div><b>Research</b><span>Freely accessible compute, storage, and GPUs for U.S. researchers and collaborators.</span></div>
    <div><b>Education</b><span>Hosted JupyterHub has become a primary access path for students and instructors.</span></div>
    <div><b>Partnerships</b><span>Vendors, government, and industry contribute hardware, data, and use cases.</span></div>
  </div>
</div>

</V2Frame>

<!--
Let's start with the elevator pitch. The simplest way I can describe NRP is "community-owned cyberinfrastructure" — and every word in that phrase matters.

Community-owned: the hardware mostly belongs to participating institutions. SDSC, Nebraska-Lincoln, MGHPCC, and Internet2 operate it as a federation. CENIC handles networking on the West Coast.

Cyberinfrastructure: it's not just compute. It's a tightly integrated stack of Kubernetes, storage, networking, identity, and software — designed to make research and teaching workloads run easily across institutions.

And it sits on three pillars: research, education, and public-private partnerships. The research mission was there from day one; the education mission is what makes NRP unusual among national-scale cyberinfrastructure; the public-private piece is how the platform keeps growing.

One important framing — Frank Würthwein, who directs SDSC, was clear at the conference that the proposal was for Kubernetes. The Jupyter explosion was a surprise. We'll come back to that.
-->

---


<V2Frame kicker="NRP AT A GLANCE" title="The numbers — as of May 2026" page="4 / 23">

<div class="v2-metric-wall">
  <div><strong>129</strong><b>sites</b><span>hosting NRP nodes across 45 U.S. states</span></div>
  <div><strong>1,532</strong><b>GPUs</b><span>shared pool; 74 reserved for LLM serving</span></div>
  <div><strong>32.3K</strong><b>CPU cores</b><span>across 501 registered Kubernetes nodes</span></div>
  <div><strong>22 PB</strong><b>storage</b><span>31 OSDF nodes; capacity to host community data</span></div>
  <div><strong>5,800</strong><b>users</b><span>past year; across 8,000+ projects</span></div>
  <div><strong>151</strong><b>JupyterHubs</b><span>90% of users reach NRP through Jupyter</span></div>
</div>

<p class="v2-source">Source: "State of NRP" keynote, Frank Würthwein, 7NRP, May 2026.</p>

</V2Frame>

<!--
These are the numbers Frank shared in his State of NRP keynote.

A few things to call out. First, the geographic footprint — 129 sites in 45 states. This isn't a regional resource. Second, the GPU number is up dramatically from 2023; that growth comes almost entirely from contributing institutions, not from NSF. Third, that 90% Jupyter figure is the surprise of the platform — only a small slice of users ever touch raw Kubernetes.

For comparison: NSF ACCESS, the primary national allocation mechanism, serves about 12,000 users per year. NRP serves roughly half that — and is growing fast. We'll come back to the comparison.

If you only remember one slide from this talk, this is a good candidate.
-->

---


<V2Frame kicker="HOW IT WORKS" title="The stack is federated; the front door is simple" page="5 / 23" bodyClass="v2-stack-slide">

<div class="v2-stack-diagram">
  <div><b>User experience</b><span>Jupyter notebooks · browser LLM chat · MCP agents</span></div>
  <div><b>Platform services</b><span>JupyterHub · vLLM · Envoy gateway · CILogon · OSDF</span></div>
  <div><b>Orchestration</b><span>Kubernetes "Nautilus" · namespaces · GPU scheduling</span></div>
  <div><b>Hardware & network</b><span>Member-site GPUs/CPUs · Pacific Wave · CENIC · Internet2</span></div>
</div>

<p class="v2-bottom-claim">Most users meet NRP through a notebook, course link, API token, or shared workspace — not Kubernetes.</p>

</V2Frame>

<!--
So how does this actually work? Picture four layers.

At the bottom: hardware contributed by member campuses, connected over research and education networks — Pacific Wave, CENIC out here in California, Internet2 nationally.

Above that: Kubernetes — the cluster is called Nautilus — plus CILogon for federated single sign-on, and namespaces to isolate institutional workloads.

Above that: platform services. JupyterHub for notebooks, vLLM serving open-weight models, an Envoy gateway that handles all the authentication and token accounting, and OSDF for object storage.

And at the top: the user experience. For 90% of people that's Jupyter in a browser. For others it's chat-style LLM access or raw Kubernetes for custom workflows.

The right side is the part that matters for IT folks: when a campus contributes hardware, NRP runs it. They handle the cluster operations, the patching, the security responses. A faculty member from CSU Fullerton at the conference said "we still have root access — we just don't have to do anything." That's the model.
-->

---


<V2Frame kicker="OPERATING MODEL" title="What NRP takes off a campus team's plate" page="6 / 23">

<div class="v2-check-grid">
  <div><b>Runs hardware from IPMI up</b><span>Campuses can contribute racks without building a full local HPC operations team.</span></div>
  <div><b>Patches the cluster</b><span>Cluster-wide security and reliability fixes happen as part of the shared service.</span></div>
  <div><b>Hosts community data</b><span>Useful datasets can be hosted free of charge for the research and education community.</span></div>
  <div><b>Provides shared services</b><span>Identity, GPU scheduling, software catalogs, chat channels, and support pathways.</span></div>
</div>

</V2Frame>

<!--
So how does this actually work? Picture four layers.

At the bottom: hardware contributed by member campuses, connected over research and education networks — Pacific Wave, CENIC out here in California, Internet2 nationally.

Above that: Kubernetes — the cluster is called Nautilus — plus CILogon for federated single sign-on, and namespaces to isolate institutional workloads.

Above that: platform services. JupyterHub for notebooks, vLLM serving open-weight models, an Envoy gateway that handles all the authentication and token accounting, and OSDF for object storage.

And at the top: the user experience. For 90% of people that's Jupyter in a browser. For others it's chat-style LLM access or raw Kubernetes for custom workflows.

The right side is the part that matters for IT folks: when a campus contributes hardware, NRP runs it. They handle the cluster operations, the patching, the security responses. A faculty member from CSU Fullerton at the conference said "we still have root access — we just don't have to do anything." That's the model.
-->

---


<V2Frame kicker="WHY JUPYTER MATTERS" title="Notebooks are how most people meet NRP" page="7 / 23">

<div class="v2-hero-plus">
  <div class="v2-big-stat"><strong>90%</strong><span>of NRP users reach the platform through Jupyter notebooks.</span><small>5,275 Jupyter users across 151 JupyterHubs.</small></div>
  <div class="v2-stack">
    <div><b>Zero local setup</b><span>Students click a link in Canvas; the environment opens in a browser.</span></div>
    <div><b>Doing, not watching</b><span>Large lectures become executable; students interact with the material.</span></div>
    <div><b>On-ramp to research</b><span>The same environment can scale from a class to graduate and faculty work.</span></div>
  </div>
</div>

</V2Frame>

<!--
This is the slide I keep coming back to.

When NRP was proposed, it was described as a Kubernetes platform — and Kubernetes was supposed to be the API. What actually happened is that JupyterHub became the front door for almost everyone. Today 90% of NRP users are Jupyter users; they may never write a YAML file in their lives.

That matters for two reasons. First, it dramatically lowers the barrier to entry. A student in an intro stats class clicks a link in Canvas and is computing. No installs, no environment hell, no package management.

Second — and this is the Frank Würthwein argument — Jupyter changes the shape of the classroom. Students stop watching the instructor work problems and start working problems themselves, in real time, on real data, even in classes with hundreds of students. UCSD has built an institution around this idea.

For us in IT: when a faculty member says "I want my students to use the cloud" or "we need GPUs for our class," nine times out of ten what they actually want is a managed Jupyter environment. NRP is one of the strongest options on the table.
-->

---

<V2Frame kicker="AI INFERENCE-AS-A-SERVICE" title="Free access to open-weight LLMs" page="8 / 23">

<div class="v2-split">
  <ol class="v2-flow">
    <li><b>nrp.ai</b><span>Single sign-on via CILogon → campus IdP</span></li>
    <li><b>nrp.ai/llmtoken</b><span>OpenAI-style bearer token</span></li>
    <li><b>API Gateway</b><span>Token check, model routing, usage logging</span></li>
    <li><b>vLLM GPU pods</b><span>10 frontier open-weight models on call (e.g. Gemma, Qwen3, GPT-OSS)</span></li>
  </ol>
  <div class="v2-callout">
    <b>Why it matters</b>
    <span>It gives research and teaching workflows a free, federated alternative to commercial inference services, with usage tied back to campus identity.</span>
  </div>
</div>

</V2Frame>

<!--
One of the most exciting developments — and a real surprise — is what NRP is doing with LLM inference.

They've stood up an OpenAI-compatible API in front of about ten frontier open-weight models — Llama, Qwen, Mistral, the usual suspects. You log in at nrp.ai with your campus credentials, generate a bearer token, and you can hit it from a Jupyter notebook, OpenWebUI, LibreChat, or your own script.

It's free for any NRP user. Mohammad Firas Sada from SDSC walked us through the architecture — there's exactly one door, one auth, one log, and Envoy handles routing and accounting.

The usage stats are striking. They've peaked at 17 billion tokens per week. Roughly $300K worth of inference in the last quarter — and 72% of that token consumption is from California. The traffic is overwhelmingly input-heavy, which means people aren't chatting with these models, they're running retrieval-augmented workflows over large documents.

The takeaway for us: if we have faculty or students who want to experiment with LLMs but can't justify OpenAI bills, this is a real option. And it works inside their Jupyter notebooks.
-->

---


<V2Frame kicker="LLM SERVICE USAGE" title="The demand signal is already visible" page="9 / 23">

<div class="v2-stat-row">
  <div><strong>17 B</strong><span>tokens / week peak</span><small>$300K of inference in the past 3 months</small></div>
  <div><strong>751</strong><span>users · 276 projects</span><small>across 35 institutions; growing ~0.5 B tokens/week</small></div>
  <div><strong>72%</strong><span>of token usage in CA</span><small>95% input-heavy → RAG, not chat</small></div>
</div>

</V2Frame>

<!--
One of the most exciting developments — and a real surprise — is what NRP is doing with LLM inference.

They've stood up an OpenAI-compatible API in front of about ten frontier open-weight models — Llama, Qwen, Mistral, the usual suspects. You log in at nrp.ai with your campus credentials, generate a bearer token, and you can hit it from a Jupyter notebook, OpenWebUI, LibreChat, or your own script.

It's free for any NRP user. Mohammad Firas Sada from SDSC walked us through the architecture — there's exactly one door, one auth, one log, and Envoy handles routing and accounting.

The usage stats are striking. They've peaked at 17 billion tokens per week. Roughly $300K worth of inference in the last quarter — and 72% of that token consumption is from California. The traffic is overwhelmingly input-heavy, which means people aren't chatting with these models, they're running retrieval-augmented workflows over large documents.

The takeaway for us: if we have faculty or students who want to experiment with LLMs but can't justify OpenAI bills, this is a real option. And it works inside their Jupyter notebooks.
-->

---


<V2Frame kicker="WHO USES NRP" title="Researchers, instructors, students" page="10 / 23">

<div class="v2-usage">
  <div class="v2-donut" aria-label="User mix: 73% R1, 25% non-R1, 2% other">
    <b class="v2-donut-a">73%</b>
    <b class="v2-donut-b">25%</b>
    <b class="v2-donut-c">2%</b>
  </div>
  <div class="v2-stack">
    <div><b>More non-R1 than R1 institutions</b><span>97 non-research-intensive institutions vs. 54 R1s.</span></div>
    <div><b>Education is the dominant workload</b><span>Most usage is classroom Jupyter, often for undergraduates in early programming classes.</span></div>
    <div><b>Free at point of use</b><span>Anyone with a U.S. institutional identity can request access; students need PI approval.</span></div>
  </div>
</div>

</V2Frame>

<!--
So who actually uses this thing?

You'd expect a national cyberinfrastructure platform to be dominated by R1 research universities. NRP isn't — and that's the most interesting fact on this slide.

73% of users are at the 54 R1 institutions on the platform. 25% are at the 97 non-R1 institutions. There are nearly twice as many non-R1 institutions participating as R1s. That ratio is unusual and intentional.

The reason is the classroom workload. NRP isn't measured in supercomputing hours; it's measured in students taught. A community college teaching intro data science can plug in just as easily as Stanford running deep-learning regulatory genomics.

The access model is simple — free at point of use for any U.S. researcher or educator. Students need a PI to authorize them, but otherwise the friction is low.

This is the part of NRP's design that I think is most worth thinking about for Cal Poly. Our profile — strong teaching, growing research, comprehensive polytechnic — is exactly the kind of institution NRP is built for.
-->

---


<V2Frame kicker="JOINING NRP" title="The on-ramp for a new campus" page="11 / 23">

<div class="v2-steps">
  <div><b>1</b><strong>Faculty explore</strong><span>A few faculty open accounts and start using shared resources.</span></div>
  <div><b>2</b><strong>Demand builds</strong><span>Interest crosses the threshold where campus hardware starts to make sense.</span></div>
  <div><b>3</b><strong>REN connects</strong><span>CENIC provisions a Science DMZ, typically 10G+.</span></div>
  <div><b>4</b><strong>NRP operates</strong><span>Campus racks hardware; NRP runs it from IPMI up.</span></div>
</div>

<p class="v2-bottom-claim">Cal Poly already has a Science DMZ in place.</p>

</V2Frame>

<!--
How does a campus actually become part of NRP?

The pattern, as Frank described it, has four stages.

First, faculty explore. A handful of curious researchers or educators just start using the platform — no contribution required, no money, no MOUs. They sign in at nrp.ai and they're working.

Second, when there's enough faculty interest, the campus decides whether to contribute hardware. This is typically a one-time capital purchase — a rack of GPU servers — that the campus owns but lets NRP operate.

Third, the regional network — CENIC for us — provisions a Science DMZ to bring that hardware online at 10 gigabits or more. Worth defining that term for this audience: a Science DMZ is a dedicated, high-throughput network segment at the campus edge, purpose-built for large research data flows. Unlike our standard CENIC connection — where traffic passes through stateful firewalls and enterprise security appliances that throttle big transfers — a Science DMZ routes science data around those bottlenecks on a friction-free path, securing it with targeted access controls and monitoring tools like perfSONAR rather than throughput-limiting firewalls. The good news is Cal Poly already has a Science DMZ, so a key piece of the NRP on-ramp is effectively already built for us.

Fourth, the NRP team takes over operations from IPMI up. The campus keeps its own namespace and root access if it wants it; what they're outsourcing is the day-to-day cluster ops, the patching, the on-call.

The CSU campuses on the platform — SDSU, San Bernardino, Fullerton, Humboldt — all followed roughly this path. We'll look at their stories next.
-->

---

<V2Frame kicker="CAL POLY TODAY" title="What's already happening at Cal Poly" page="12 / 23">

<div class="v2-metric-wall compact">
  <div><strong>8</strong><b>active namespaces</b></div>
  <div><strong>8</strong><b>unique PIs</b></div>
  <div><strong>16K</strong><b>GPU hours</b></div>
  <div><strong>251K</strong><b>CPU hours</b></div>
  <div><strong>98</strong><b>avg GPU hrs / day</b></div>
  <div><strong>1K</strong><b>avg CPU hrs / day</b></div>
</div>
<p style="font-style: italic;"> Active NRP usage over the past 12 months. </p>
<p class="v2-source">Source: NRP Grafana usage dashboard, Cal Poly namespaces, May 2026.</p>

</V2Frame>

<!--
When I first drafted this talk I only knew of one Cal Poly researcher on NRP — Lauren Chan. Since then I've become an admin of the Cal Poly root namespace, with access to the NRP Grafana usage dashboards, and the real picture is much richer.

We have 8 active namespaces, 8 unique PIs, and roughly 16,000 GPU hours and 251,000 CPU hours of activity. GPU usage is dominated by Paul Anderson's lab, with Lauren Chan's lab second; CPU usage is spread broadly across all eight researchers — Anderson, Appleby, Chan, Pantoja, Ruiz, Villafana, Farzan, and my own test namespace.

The striking thing is that all of this happened organically — these researchers found NRP and started using it with no central ITS involvement at all. That's both the headline and the opportunity: there's real, broad-based demand here that we could be supporting and accelerating.

On the right is one researcher's work in depth. Lauren Chan in Evolutionary Biology does conservation computational genomics — reference-genome decontamination, variant calling across full genomes for a hundred individuals — and her lab has logged 892 GPU hours and 27.3K CPU hours to date. Larry Smarr highlighted her work in the "Whirlwind Tour of Science" session at the conference.

I'll come back to specific opportunities for ITS later in the talk.
-->

---


<V2Frame kicker="RESEARCH HIGHLIGHT" title="Lauren Chan — Cal Poly SLO" page="13 / 23">

<div class="v2-split">
  <div class="v2-callout">
    <b>Evolutionary Biology & Conservation Computational Genomics</b>
    <span>Research featured in "Whirlwind Tour of Science on NRP," Larry Smarr, 7NRP 2026.</span>
  </div>
  <div class="v2-list">
    <p>892 GPU hours and 27.3K CPU hours to date</p>
    <p>Reference-genome decontamination on high-memory nodes</p>
    <p>Variant calling across full genomes for 100 individuals</p>
    <p>Post-calling filtering and downstream analysis</p>
  </div>
</div>

</V2Frame>

<!--
When I first drafted this talk I only knew of one Cal Poly researcher on NRP — Lauren Chan. Since then I've become an admin of the Cal Poly root namespace, with access to the NRP Grafana usage dashboards, and the real picture is much richer.

We have 8 active namespaces, 8 unique PIs, and roughly 16,000 GPU hours and 251,000 CPU hours of activity. GPU usage is dominated by Paul Anderson's lab, with Lauren Chan's lab second; CPU usage is spread broadly across all eight researchers — Anderson, Appleby, Chan, Pantoja, Ruiz, Villafana, Farzan, and my own test namespace.

The striking thing is that all of this happened organically — these researchers found NRP and started using it with no central ITS involvement at all. That's both the headline and the opportunity: there's real, broad-based demand here that we could be supporting and accelerating.

On the right is one researcher's work in depth. Lauren Chan in Evolutionary Biology does conservation computational genomics — reference-genome decontamination, variant calling across full genomes for a hundred individuals — and her lab has logged 892 GPU hours and 27.3K CPU hours to date. Larry Smarr highlighted her work in the "Whirlwind Tour of Science" session at the conference.

I'll come back to specific opportunities for ITS later in the talk.
-->

---


<V2Frame kicker="CSU SISTER CAMPUSES" title="Three operating models to learn from" page="14 / 23">

<div class="v2-card-row">
  <div><b>SDSU</b><strong>VERNE + TIDE</strong><span>Instructional cluster, JupyterHub front-end, student-assistant support model.</span><em>Demand creation is the hard part.</em></div>
  <div><b>CSU San Bernardino</b><strong>BOT model</strong><span>Build, Operate, Transfer for partners; preconfigured JupyterHubs.</span><em>Stage resources ahead of demand.</em></div>
  <div><b>CSU Fullerton</b><strong>Faculty enablement</strong><span>IT + faculty + Academic Affairs; modules co-designed with instructional designers.</span><em>Jupyter is not just for STEM.</em></div>
</div>

</V2Frame>

<!--
The most useful session for me personally was the CSU panel — Kyle Krick from SDSU, Dung Vu from San Bernardino, and Dhusdee Chandswang from Fullerton. Three campuses, three approaches, all worth borrowing from.

SDSU built a named instructional cluster called VERNE — $650K, with JupyterHub on top and student assistants doing tier-one support. Their hard-won lesson was the obvious one in retrospect: just because you build it doesn't mean they will come. Demand creation, faculty engagement, and instructor onboarding turned out to be the real work.

San Bernardino has the most interesting model: Build, Operate, Transfer. They stand up a JupyterHub for a partner — a community college, or in their case Loma Linda University — run it during the term, and gradually hand it over. They've built playbooks for staging resources ahead of demand.

Fullerton went big on faculty enablement. The IT shop partnered with Academic Affairs and the colleges to co-design reusable course modules with instructional designers. Their key insight: Jupyter is not just for STEM. Once you've got the infrastructure, you can put humanities and social science faculty on it too.

Three different routes, same destination — and all useful patterns if we decide to go deeper.
-->

---


<V2Frame kicker="WHAT GETS DONE ON NRP" title="Science examples, part 1" page="15 / 23">

<div class="v2-card-row">
  <div><b>Agriculture</b><strong>AIIRA & Iron Horse Vineyard</strong><span>InsectNet/WeedNet foundation models and a connected vineyard testbed.</span></div>
  <div><b>Wildfire</b><strong>BurnPro3D</strong><span>Operational 3D fire and smoke modeling for prescribed burns.</span></div>
  <div><b>Climate</b><strong>JAX-based climate emulators</strong><span>Portable models running on CPU/GPU/TPU, bridging observations and simulation.</span></div>
</div>

</V2Frame>

<!--
I'm going to fly through this. Six science vignettes — three from the CSUs, three from elsewhere.

AIIRA out of Iowa State trained pest and weed identification models with 200,000 GPU hours on the DGX cloud and now serves InsectNet through a web app with 98% accuracy across 3,800 species. The Iron Horse vineyard in Sonoma is a CENIC-connected living lab where the vineyard owner calls AI "the new tractor."

BurnPro3D runs full 3D fire and smoke simulations to plan prescribed burns. CAL FIRE is using it operationally. It only became possible because NRP gives them elastic compute they couldn't get on a traditional supercomputer schedule.

JAX climate emulators from Duncan Watson-Parris at Scripps are rewriting legacy Fortran climate models in differentiable Python, runnable on any accelerator. Deep learning is being used to mine satellite imagery for cloud morphology.

On the health side, a CSU Fullerton graduate student used 4,500 GPU hours building an Alzheimer's classification pipeline on brain MRIs across 1,200 participants.

San Bernardino is running 50,000 GPU hours of VASP for quantum molecular dynamics — and Cal Poly's Lauren Chan is on the same infrastructure as Stanford's Anshul Kundaje, who used 130,000 GPU hours decoding regulatory genomics.

The point isn't the specific projects. It's the breadth — climate to materials to genomics to wildfire, R1s and CSUs side by side.
-->

---


<V2Frame kicker="WHAT GETS DONE ON NRP" title="Science examples, part 2" page="16 / 23">

<div class="v2-card-row">
  <div><b>Health</b><strong>Brain MRI for Alzheimer's</strong><span>CSU Fullerton: 4,500 GPU hours across 1,200 participants.</span></div>
  <div><b>Materials</b><strong>Quantum molecular dynamics</strong><span>CSUSB: VASP simulations using custom JupyterHubs and 50K GPU hours/year.</span></div>
  <div><b>Genomics</b><strong>Deep regulatory genomics</strong><span>Stanford and Cal Poly work decoding gene regulation on the same platform.</span></div>
</div>

</V2Frame>

<!--
I'm going to fly through this. Six science vignettes — three from the CSUs, three from elsewhere.

AIIRA out of Iowa State trained pest and weed identification models with 200,000 GPU hours on the DGX cloud and now serves InsectNet through a web app with 98% accuracy across 3,800 species. The Iron Horse vineyard in Sonoma is a CENIC-connected living lab where the vineyard owner calls AI "the new tractor."

BurnPro3D runs full 3D fire and smoke simulations to plan prescribed burns. CAL FIRE is using it operationally. It only became possible because NRP gives them elastic compute they couldn't get on a traditional supercomputer schedule.

JAX climate emulators from Duncan Watson-Parris at Scripps are rewriting legacy Fortran climate models in differentiable Python, runnable on any accelerator. Deep learning is being used to mine satellite imagery for cloud morphology.

On the health side, a CSU Fullerton graduate student used 4,500 GPU hours building an Alzheimer's classification pipeline on brain MRIs across 1,200 participants.

San Bernardino is running 50,000 GPU hours of VASP for quantum molecular dynamics — and Cal Poly's Lauren Chan is on the same infrastructure as Stanford's Anshul Kundaje, who used 130,000 GPU hours decoding regulatory genomics.

The point isn't the specific projects. It's the breadth — climate to materials to genomics to wildfire, R1s and CSUs side by side.
-->

---


<V2Frame kicker="EDUCATION AT SCALE" title="UCSD shows what digital assets can become" page="17 / 23">

<div class="v2-hero-plus">
  <div class="v2-big-stat navy"><strong>30,000</strong><span>students per year on UCSD DataHub, across 30 departments.</span></div>
  <div class="v2-timeline">
    <div><b>2017</b><strong>Free compute for instructors</strong><span>Shared notebook infrastructure free at point of use.</span></div>
    <div><b>2024</b><strong>AI tutors per class</strong><span>Personalized tutors across multiple large courses.</span></div>
    <div><b>2026</b><strong>Free AI for instructors</strong><span>Open-weight LLMs at the same scale.</span></div>
  </div>
</div>

</V2Frame>

<!--
If you want to see what "digital assets in the classroom" looks like at scale, UCSD is the case study.

30,000 students per year on their DataHub. 30 departments. Sam Lau showed us a Music and Machine Learning class with 1,523 students in a single section, all in Jupyter notebooks.

The history here is instructive. In 2017 UCSD asked the question "what happens if we make compute free for instructors?" The answer was that the whole institution reorganized around it.

In 2025 they rolled out personalized AI tutors across multiple large courses. The argument from Frank Würthwein, who's not exactly a softie, was blunt — "colleges that fail to adopt these methods will go bankrupt."

I'm not asking you to agree with him. But the framing matters: human beings learn better by doing than by watching, and digital assets — notebooks and tutors and LLMs — are what make doing possible in a 1,500-person lecture hall.

The 2026 experiment at UCSD is "what happens if we make AI free for instructors?" That experiment is running on the same NRP infrastructure I described two slides ago.
-->

---


<V2Frame kicker="COMMUNITY COLLEGES & EQUITY" title="The California transfer pipeline is the scale problem" page="18 / 23">

<div class="v2-pipeline">
  <div><b>K–12</b><strong>2M+</strong><span>public high schoolers</span></div>
  <div><b>CCC</b><strong>2.2M</strong><span>students across 116 colleges</span></div>
  <div><b>CSU</b><strong>480K</strong><span>students across 23 campuses</span></div>
  <div><b>UC</b><strong>440K</strong><span>students across 10 campuses</span></div>
</div>

<p class="v2-bottom-claim">30% of U.S. transfer students come from California community colleges. If CSUs and UCs deploy digital assets but CCCs cannot match them, the pipeline breaks.</p>

</V2Frame>

<!--
This slide is the part of the conference that stuck with me most.

California has the strongest community college system in the country — 2.2 million students across 116 colleges, more than the CSUs and UCs combined. 30% of all U.S. transfer students come out of CCCs. Half of every CSU incoming class is a transfer student.

So when UCSD or Stanford gives every undergraduate a personalized AI tutor and a Jupyter environment, the question is what happens to the student transferring in from Cuesta or Allan Hancock who's never seen any of it.

Sean Michael Morris from UC Berkeley walked us through their Data8 outreach — 3,000 students per semester, now reaching 27 California community colleges, 2 high schools, and 11 CSUs and UCs. It's free, the notebooks are open-source, the infrastructure runs on CloudBank.

For Cal Poly — given our strong transfer relationship with Cuesta and Allan Hancock — this is exactly the kind of work that's directly relevant. And IT can play a real role on two fronts. First, the unglamorous plumbing: identity federation, single sign-on, the connectivity that makes pipelines like this work. Second — and this is newer — we're making real program investments. In partnership with the Noyce School of Applied Computing, ITS is standing up focused academic and research computing support, so this kind of work has a dedicated home in IT rather than depending on individual faculty to navigate it alone.
-->

---


<V2Frame kicker="BROADER LANDSCAPE" title="Where NRP sits in U.S. research computing" page="19 / 23">

<table class="v2-table">
  <thead><tr><th></th><th>NRP</th><th>ACCESS</th><th>NAIRR</th><th>NERSC</th><th>NDP</th></tr></thead>
  <tbody>
    <tr><th>Purpose</th><td>Research + education</td><td>NSF compute allocations</td><td>AI research resource</td><td>DOE leadership computing</td><td>Federated AI-ready data</td></tr>
    <tr><th>Access</th><td>Open at point of use</td><td>Proposal-based</td><td>3-page request</td><td>DOE-aligned PI allocation</td><td>Federation; API + endpoints</td></tr>
    <tr><th>Scale</th><td>5,800 users · 8K+ projects</td><td>12K users / yr</td><td>700+ projects · 6K+ students</td><td>11K researchers / yr</td><td>Data + workspaces</td></tr>
    <tr><th>What you get</th><td>K8s + Jupyter + LLMs</td><td>Many systems</td><td>Academic + industry GPUs</td><td>Leadership systems</td><td>Catalogs, classrooms</td></tr>
  </tbody>
</table>

</V2Frame>

<!--
Where does NRP fit in the larger research computing ecosystem?

The simplest way to think about it: there's a small constellation of national-scale platforms, and NRP is the one purpose-built for breadth — both research and education, both R1s and non-R1s.

NSF ACCESS is the umbrella allocation system — about 12,000 users a year, very proposal-driven. NAIRR is the federal AI testbed that grew out of the CHIPS Act conversation; about 700 active projects, 6,000+ students. NERSC is the DOE Office of Science workhorse — Perlmutter and its successors, very different audience.

NDP — the National Data Platform — is something I haven't said much about yet. It's the data layer designed to sit alongside NRP. Ilkay Altintas's argument at the conference was that GPUs alone aren't AI infrastructure — what's missing is data readiness, knowledge graphs, and agentic workflows. NDP is the answer. Increasingly NRP and NDP are referenced as a pair.

For our purposes: NRP is the one with the broadest open access model, the most education focus, and the most direct California presence. NAIRR is worth tracking; it's where the federal AI investment is flowing.
-->

---


<V2Frame kicker="WHERE THIS IS GOING" title="Agents, data, and an AI-ready ecosystem" page="20 / 23">

<div class="v2-check-grid">
  <div><b>Agentic AI on trusted infrastructure</b><span>Agents that discover data, assemble workflows, and act on scientific systems.</span></div>
  <div><b>Federation of NRP + NDP</b><span>Endpoints anywhere, connected to a national catalog. Workflow is not teamflow.</span></div>
  <div><b>Edge to HPC continuum</b><span>Sensors, drones, inference, JupyterHubs, and leadership-class systems in one ecosystem.</span></div>
  <div><b>Sustaining the pilots</b><span>NAIRR moves toward at-scale; NRP explores longer-term funding models.</span></div>
</div>

</V2Frame>

<!--
A few words on where I think this is headed, based on what I heard at the conference.

First — and this came up in almost every keynote — the next wave isn't better chatbots. It's agentic AI sitting on top of trusted national-scale scientific infrastructure. The argument from Ilkay Altintas at SDSC was that GPUs alone are not AI infrastructure; you need workflows, governance, knowledge graphs, and data lineage. NDP is being built explicitly for that.

Second, the federation of NRP and NDP is increasingly explicit. NDP endpoints — lightweight catalog and workspace services — are designed to be deployable anywhere, including on a campus, an edge device, or a cloud. The phrase that stuck with me was "workflow is not teamflow."

Third, the same ecosystem now spans from a vineyard sensor in Sebastopol up through campus GPU clusters to NSF's Leadership Class Computing Facility coming online with 4,000 Blackwell GPUs.

Fourth — and this is the bit that touches all of us — the sustainability picture is genuinely uncertain. NSF is open and making awards, but it's reorganizing. NAIRR is on a path from pilot to foundation to at-scale. NRP is itself part of that conversation.

The short version: things are moving, the architecture is converging, and now is a reasonable time to pay attention.
-->

---


<V2Frame kicker="KEY TAKEAWAYS" title="What I’d like you to walk away with" page="21 / 23">

<div class="v2-takeaways">
  <div><b>NRP is real, free, and growing fast.</b><span>129 sites · 1,532 GPUs · 5,800 users · 90% through Jupyter.</span></div>
  <div><b>Kubernetes is the substrate; Jupyter is the front door.</b><span>The interesting layer is the notebook and service experience.</span></div>
  <div><b>Research and education are now side by side.</b><span>The same platform can serve classrooms, labs, and AI workflows.</span></div>
  <div><b>California is central — and Cal Poly fits the profile.</b><span>CENIC is the network; sister CSUs are already running playbooks.</span></div>
  <div><b>The boundaries are dissolving.</b><span>This crosses research, education, IT, data, and AI strategy.</span></div>
</div>

</V2Frame>

<!--
Five takeaways to leave you with.

One: NRP is real and operating at meaningful scale. Cal Poly is already on it through at least one researcher. The cost of exploring more is zero.

Two: Kubernetes is the substrate but Jupyter is the front door for almost everyone. If we're going to engage, the question isn't "do we run Kubernetes" — it's "do we make Jupyter easy for our faculty and students."

Three: NRP genuinely serves both research and education. Jupyter is what makes it accessible, and it's how the majority of users get in — but I don't want to overstate it. A significant portion of actual cluster usage happens through other Kubernetes-based methods. The user counts and the usage counts tell slightly different stories, and I haven't found clean statistics that cleanly separate the two. The real point is breadth: NRP supports teaching and research at once, which is a strong fit for a comprehensive polytechnic like ours.

Four: California — and especially the CSU system — is central to the NRP story. CENIC is the network. SDSU, CSUSB, Fullerton, and Humboldt are already on the platform. We have ready peers to learn from.

Five: this work doesn't fit neatly into the boxes IT typically uses. It's part research computing, part academic technology, part identity and security, part network engineering, part data governance. Some of the most interesting opportunities sit in the seams between those teams — including the one we're in right now.
-->

---


<V2Frame kicker="RESOURCES" title="Where to learn more" page="22 / 23">

<div class="v2-resource-grid">
  <div><b>nrp.ai</b><span>Platform access, namespaces, docs</span></div>
  <div><b>nrp.ai/llmtoken</b><span>Generate an LLM API token</span></div>
  <div><b>nationaldataplatform.org</b><span>NDP catalog, classrooms, federation docs</span></div>
  <div><b>nairrpilot.org</b><span>NAIRR resource request form</span></div>
  <div><b>dash.nrp-nautilus.io</b><span>NRP dashboard and Grafana metrics</span></div>
  <div><b>data8.org / data6</b><span>Open intro data science curriculum</span></div>
</div>

<p class="v2-bottom-claim">Want to talk further? brianspo@calpoly.edu · Slides and notes available on request.</p>

</V2Frame>

<!--
A short resource page so you have something to take with you.

The single most useful link is nrp.ai itself — you can sign in with your campus credentials and start exploring inside of five minutes. nrp.ai/llmtoken gets you an LLM API token if you want to play with that.

The National Data Platform is at nationaldataplatform.org — they're running an educator workshop in early August if you're interested. NAIRR resource requests are a three-page form with a six-week turnaround, much lighter weight than a full NSF proposal.

For the curricular side, data8.org has the open course materials, and the Carpentries are still the best general community for teaching computational skills. SDSC's Societal Computing & Innovation Lab — scil.ucsd.edu — is where the wildfire and climate work I mentioned is centered.

And of course, please reach out. I have notes from every session, contacts at SDSU, San Bernardino, Fullerton, and SDSC who've offered to help, and I'd much rather have a conversation than answer questions in chat.
-->

---


<V2Frame dark :footer="false" bodyClass="v2-cover">

<p class="v2-cover-kicker">QUESTIONS</p>

# What's catching your attention?

<p class="v2-cover-meta"><strong>Brian Spolarich</strong> · brianspo@calpoly.edu · ITS AI Community of Practice</p>

</V2Frame>

<!--
Thank you. I'd love to hear what's catching your attention — whether that's a particular use case, a question about how we'd actually get hardware on the platform, or a connection to something you're working on.

A few prompts in case nothing jumps out:

— Do any of you know Cal Poly faculty already using NRP? I'd love to be connected.
— Where do you see the most natural starting point for ITS engagement — identity federation, networking, namespace operations, faculty support?
— Are there CSU or CCC partnerships in your part of the org that we should be coordinating with?

Floor is open.
-->
