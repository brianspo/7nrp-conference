---
theme: default
layout: default
title: The National Research Platform - Native Slidev
class: nrp-native
transition: fade
canvasWidth: 980
aspectRatio: 16/9
favicon: false
fonts:
  sans: Arial
---

<NativeFrame dark :footer="false" bodyClass="cover-body">

<div class="cover-kicker">THE NATIONAL RESEARCH PLATFORM</div>

# Insights from 7NRP, and what they mean for Cal Poly

<p class="cover-byline"><strong>Brian Spolarich</strong> · ITS AI Community of Practice · May 2026</p>

</NativeFrame>

---

<NativeFrame kicker="AGENDA" title="What we'll cover" page="2 / 19">

<div class="agenda-native">
  <div><b>1</b><strong>What NRP is</strong><span>Vision, scale, and the headline numbers</span></div>
  <div><b>2</b><strong>How it works</strong><span>Kubernetes, Jupyter, and a federated REN backbone</span></div>
  <div><b>3</b><strong>Who uses it — and how</strong><span>Researchers, educators, students; LLM service</span></div>
  <div><b>4</b><strong>Cal Poly & the CSUs today</strong><span>Where we are; what SDSU, CSUSB, and CSUF are doing</span></div>
  <div><b>5</b><strong>The broader landscape</strong><span>NRP vs. ACCESS, NAIRR, NERSC, NDP</span></div>
  <div><b>6</b><strong>Takeaways</strong><span>What's interesting; questions for our group</span></div>
</div>

</NativeFrame>

---

<NativeFrame kicker="WHAT IS NRP" title="Community-owned cyberinfrastructure" page="3 / 19">

<div class="two-col quote-layout">
  <div class="quote-card">
    <p>"A global-scale Kubernetes cluster for research, education, and public-private partnerships — built and run by the community it serves."</p>
    <small>— Frank Würthwein, Director, San Diego Supercomputer Center</small>
    <p class="note">Operated jointly by SDSC (UCSD), the University of Nebraska–Lincoln, MGHPCC, and Internet2 — with Pacific Wave / CENIC providing networking.</p>
  </div>
  <div class="feature-stack">
    <div><strong>Research</strong><span>Freely accessible compute, storage, and GPUs for U.S. researchers and their collaborators.</span></div>
    <div><strong>Education</strong><span>NRP's hosted JupyterHub — unplanned at launch, now a primary access path — is built for students and instructors.</span></div>
    <div><strong>Public–private partners</strong><span>Vendors, government, and industry contribute hardware, data, and use cases.</span></div>
  </div>
</div>

</NativeFrame>

---

<NativeFrame kicker="NRP AT A GLANCE" title="The numbers — as of May 2026" page="4 / 19">

<div class="metric-grid">
  <div><strong>129</strong><b>sites</b><span>hosting NRP nodes across 45 U.S. states</span></div>
  <div><strong>1,532</strong><b>GPUs</b><span>shared pool; 74 reserved for LLM serving</span></div>
  <div><strong>32.3K</strong><b>CPU cores</b><span>across 501 registered Kubernetes nodes</span></div>
  <div><strong>22 PB</strong><b>storage</b><span>31 OSDF nodes; capacity to host community data</span></div>
  <div><strong>5,800</strong><b>users (past year)</b><span>across 8,000+ projects; freely accessible in U.S.</span></div>
  <div><strong>151</strong><b>JupyterHubs</b><span>90% of NRP users reach the platform through Jupyter</span></div>
</div>

<p class="source">Source: "State of NRP" keynote, Frank Würthwein, 7NRP, May 2026.</p>

</NativeFrame>

---

<NativeFrame kicker="HOW IT WORKS" title="A federated Kubernetes cluster with Jupyter on top" page="5 / 19">

<div class="two-col platform-layout">
  <div class="layer-stack">
    <div><strong>User experience</strong><span>Jupyter notebooks, browser-based LLM chat, MCP agents</span></div>
    <div><strong>Platform services</strong><span>JupyterHub, vLLM, Envoy API gateway, CILogon identity, OSDF storage</span></div>
    <div><strong>Orchestration</strong><span>Kubernetes ("Nautilus"), namespaces, GPU scheduling</span></div>
    <div><strong>Hardware & network</strong><span>GPUs/CPUs at member sites, Pacific Wave / CENIC / Internet2</span></div>
  </div>
  <div class="bullet-panel">
    <h3>What NRP does for you</h3>
    <ul>
      <li>Runs your hardware from IPMI up</li>
      <li>Patches the cluster automatically</li>
      <li>Hosts community-useful data free of charge</li>
      <li>Provides identity, GPU scheduling, and a software catalog</li>
      <li>Operates topical chat channels — a "permanent digital water cooler"</li>
    </ul>
  </div>
</div>

</NativeFrame>

---

<NativeFrame kicker="WHY JUPYTER MATTERS" title="Notebooks are the way most people meet NRP" page="6 / 19">

<div class="two-col jupyter-layout">
  <div class="hero-stat">
    <strong>90%</strong>
    <span>of NRP users reach the platform through Jupyter notebooks.</span>
    <small>5,275 Jupyter users across 151 JupyterHubs.</small>
  </div>
  <div class="feature-stack">
    <div><strong>Zero local setup</strong><span>Students click a link in Canvas; a containerized environment opens in their browser.</span></div>
    <div><strong>Doing, not watching</strong><span>Jupyter brings interactivity back to large lectures — students execute, not just observe.</span></div>
    <div><strong>Scalability</strong><span>Instructors share containers and notebooks; a new instructor can be up and running in as little as a one-hour session.</span></div>
    <div><strong>On-ramp to research</strong><span>Same environment scales from a classroom teaching hub to graduate and faculty research workspaces.</span></div>
  </div>
</div>

</NativeFrame>

---

<NativeFrame kicker="AI INFERENCE-AS-A-SERVICE" title="Free, federated access to open-weight LLMs" page="7 / 19">

<div class="two-col ai-layout">
  <div>
    <h3>How it works</h3>
    <ol class="numbered-flow">
      <li><strong>nrp.ai</strong><span>Single sign-on via CILogon → your campus IdP</span></li>
      <li><strong>nrp.ai/llmtoken</strong><span>OpenAI-style API bearer token</span></li>
      <li><strong>API Gateway (envoyproxy.io)</strong><span>Token check, model routing, usage logging</span></li>
      <li><strong>vLLM pods (GPU)</strong><span>10 frontier open-weight models on call</span></li>
    </ol>
  </div>
  <div>
    <h3>Usage today</h3>
    <div class="compact-stats">
      <div><strong>17 B</strong><span><b>tokens / week peak</b>$300K of inference in past 3 months</span></div>
      <div><strong>751</strong><span><b>users · 276 projects</b>across 35 institutions; growing ~0.5 B tokens/week</span></div>
      <div><strong>72%</strong><span><b>of token usage in CA</b>95% input-heavy → RAG, not chat</span></div>
    </div>
  </div>
</div>

</NativeFrame>

---

<NativeFrame kicker="WHO USES NRP" title="Researchers, instructors, students" page="8 / 19">

<div class="two-col users-layout">
  <div class="native-donut" style="--a: 73%; --b: 25%;">
    <b class="slice-label label-a">73%</b>
    <b class="slice-label label-b">25%</b>
    <b class="slice-label label-c">2%</b>
  </div>
  <div class="feature-stack gold">
    <div><strong>More non-R1 than R1 institutions</strong><span>97 non-research-intensive institutions vs. 54 R1s — flipping the usual cyberinfrastructure pattern.</span></div>
    <div><strong>Education is the dominant workload</strong><span>Most usage is classroom Jupyter — undergraduates, often in their first programming class.</span></div>
    <div><strong>Geographic reach is broad</strong><span>Users from 45 states. NAIRR data shows similar reach — 6,000+ students across all 50.</span></div>
    <div><strong>Free at point of use</strong><span>Anyone with a U.S. institutional identity can request access; students need PI approval.</span></div>
  </div>
</div>

</NativeFrame>

---

<NativeFrame kicker="JOINING NRP" title="The on-ramp for a new campus" page="9 / 19">

<div class="step-cards">
  <div><header><b>1</b><strong>Faculty explore</strong></header><p>A few faculty open accounts and start using shared NRP resources. No cost; free at point of use.</p></div>
  <div><header><b>2</b><strong>Demand builds</strong></header><p>When interest crosses a threshold, the campus considers contributing hardware to NRP.</p></div>
  <div><header><b>3</b><strong>REN connects</strong></header><p>The regional research network (CENIC for us) provisions a Science DMZ — typically 10G+.</p><em>Cal Poly already has a Science DMZ in place</em></div>
  <div><header><b>4</b><strong>NRP operates</strong></header><p>Campus racks hardware. NRP team runs it from IPMI up. Campus-owned Kubernetes namespace and root.</p></div>
</div>

<p class="source">Operating model: "Your REN provider owns the network. NRP runs the hardware. Your researchers, educators, and students see a global-scale Kubernetes cluster."</p>

</NativeFrame>

---

<NativeFrame kicker="CAL POLY TODAY" title="What's already happening at Cal Poly" page="10 / 19">

<div class="two-col calpoly-layout">
  <div>
    <h3>Usage snapshot</h3>
    <div class="mini-metrics">
      <div><strong>8</strong><span>active namespaces</span></div>
      <div><strong>8</strong><span>unique PIs</span></div>
      <div><strong>16K</strong><span>GPU hours</span></div>
      <div><strong>251K</strong><span>CPU hours</span></div>
      <div><strong>98</strong><span>avg GPU hrs / day</span></div>
      <div><strong>1K</strong><span>avg CPU hrs / day</span></div>
    </div>
    <p class="note"><b>Top GPU users:</b> Anderson Lab (8.6K hrs) and Chan Lab (892 hrs). CPU usage is broad-based across all 8 PIs.</p>
  </div>
  <div class="research-card">
    <h3>Research highlight</h3>
    <h2>Lauren Chan — Cal Poly SLO</h2>
    <p>Evolutionary Biology & Conservation Computational Genomics</p>
    <ul>
      <li>892 GPU hours and 27.3K CPU hours to date</li>
      <li>Reference-genome decontamination on high-memory nodes</li>
      <li>Variant calling across full genomes for 100 individuals</li>
      <li>Post-calling filtering and downstream analysis</li>
    </ul>
  </div>
</div>

</NativeFrame>

---

<NativeFrame kicker="CSU SISTER CAMPUSES" title="Three CSUs, three operating models" page="11 / 19">

<div class="three-cards">
  <div><h2>SDSU</h2><b>VERNE + TIDE</b><p>Instructional cluster ($650K), JupyterHub front-end, student-assistant support model.</p><strong>Lesson learned</strong><span>"Just because you build it doesn't mean they will come." Demand-creation is the hard part.</span></div>
  <div><h2>CSU San Bernardino</h2><b>BOT model</b><p>Build, Operate, Transfer: SBValley CC and Loma Linda; preconfigured JupyterHubs for partners.</p><strong>Lesson learned</strong><span>Stage HPC resources ahead of demand; engage admins and faculty early.</span></div>
  <div><h2>CSU Fullerton</h2><b>Faculty enablement</b><p>IT + faculty + Academic Affairs partnership. Course modules co-designed with instructional designers.</p><strong>Lesson learned</strong><span>"Jupyter is not just for STEM." Reusable course modules accelerate adoption.</span></div>
</div>

</NativeFrame>

---

<NativeFrame kicker="WHAT GETS DONE ON NRP" title="A sample of the science" page="12 / 19">

<div class="science-grid">
  <div><b>Agriculture</b><strong>AIIRA & Iron Horse Vineyard</strong><span>InsectNet/WeedNet foundation models; 10G-connected vineyard testbed with drones, sensors, and edge inference.</span></div>
  <div><b>Wildfire</b><strong>BurnPro3D</strong><span>Operational 3D fire and smoke modeling for prescribed burns, with bursty elastic compute.</span></div>
  <div><b>Climate</b><strong>JAX-based climate emulators</strong><span>Differentiable, portable climate models running on CPU/GPU/TPU.</span></div>
  <div><b>Health</b><strong>Brain MRI for Alzheimer's</strong><span>CSU Fullerton work across 1,200 participants, using 4,500 GPU hours.</span></div>
  <div><b>Materials</b><strong>Quantum molecular dynamics</strong><span>CSUSB custom JupyterHubs for VASP simulations, 50K GPU hours/year.</span></div>
  <div><b>Genomics</b><strong>Deep regulatory genomics</strong><span>Stanford and Cal Poly work decoding gene regulation on the same platform.</span></div>
</div>

</NativeFrame>

---

<NativeFrame kicker="EDUCATION AT SCALE" title="UCSD's case for digital assets in the classroom" page="13 / 19">

<div class="two-col education-layout">
  <div class="hero-stat navy">
    <strong>30,000</strong>
    <span>students per year on UCSD DataHub, across 30 departments.</span>
    <small>1,523 students in a single Music + Machine Learning class (Spring 2025). — Sam Lau, UCSD</small>
  </div>
  <div class="timeline">
    <div><b>2017</b><strong>Free compute for instructors</strong><span>Shared notebook infrastructure free at point of use for any course.</span></div>
    <div><b>2024</b><strong>AI tutors per class</strong><span>Fall 2025 rollout of personalized AI tutors across multiple large courses.</span></div>
    <div><b>2026</b><strong>Free AI for instructors</strong><span>Experimenting with open-weight LLMs at the same scale — same question, new tool.</span></div>
  </div>
</div>

</NativeFrame>

---

<NativeFrame kicker="COMMUNITY COLLEGES & EQUITY" title="Why NRP cares about the CA transfer pipeline" page="14 / 19">

<div class="pipeline">
  <div><b>K–12</b><strong>2M+</strong><span>Public high schoolers; many take CCC dual enrollment</span></div>
  <div><b>CCC</b><strong>2.2M</strong><span>Students across 116 California community colleges</span></div>
  <div><b>CSU</b><strong>480K</strong><span>Students across 23 CSU campuses</span></div>
  <div><b>UC</b><strong>440K</strong><span>Students across 10 UC campuses</span></div>
</div>

<div class="callout-band">
  <strong>Why this matters</strong>
  <span>30% of all U.S. transfer students come from California community colleges. 50% of every incoming CSU class arrived as a transfer. If CSUs and UCs deploy digital assets in the classroom but CCCs can't match, the pipeline breaks. NRP's Data8 partnership has reached 27 CCCs, 2 high schools, and 11 CSUs/UCs.</span>
</div>

</NativeFrame>

---

<NativeFrame kicker="BROADER LANDSCAPE" title="Where NRP sits in U.S. research computing" page="15 / 19">

<table class="comparison-table">
  <thead><tr><th></th><th>NRP</th><th>NSF ACCESS</th><th>NAIRR pilot</th><th>NERSC</th><th>NDP</th></tr></thead>
  <tbody>
    <tr><th>Primary purpose</th><td>Research + education</td><td>Allocations to NSF compute</td><td>AI research resource</td><td>DOE leadership computing</td><td>Federated AI-ready data</td></tr>
    <tr><th>Access model</th><td>Open at point of use</td><td>Proposal-based allocation</td><td>3-page resource request</td><td>DOE-aligned PI allocation</td><td>Federation; API + endpoints</td></tr>
    <tr><th>Scale</th><td>5,800 users · 8K+ projects</td><td>12K users / yr</td><td>700+ projects · 6K+ students</td><td>11K researchers / yr</td><td>Federated data + workspaces</td></tr>
    <tr><th>What you get</th><td>K8s + Jupyter + LLMs</td><td>Many systems, varying</td><td>Industry & academic GPUs</td><td>Perlmutter, Cori successors</td><td>Data catalogs, classrooms</td></tr>
  </tbody>
</table>

<p class="source">Notes: ACCESS is the primary NSF allocation gateway. NAIRR is the federal AI testbed. NERSC is the DOE Office of Science compute center. NDP is the data layer that increasingly works alongside NRP.</p>

</NativeFrame>

---

<NativeFrame kicker="WHERE THIS IS GOING" title="What's next: agents, data, and an AI-ready ecosystem" page="16 / 19">

<ol class="big-list">
  <li><strong>Agentic AI on top of trusted infrastructure</strong><span>Not better chatbots — agents that discover data, assemble workflows, and act on national-scale scientific systems.</span></li>
  <li><strong>Federation of NRP + NDP</strong><span>NDP endpoints deployable anywhere — campus, edge, cloud — connected to a national catalog. "Workflow is not teamflow."</span></li>
  <li><strong>From edge to HPC, one continuum</strong><span>Sage Grande sensors, drones in vineyards, AI inference in a winery, JupyterHubs on shared GPUs, and leadership-class systems.</span></li>
  <li><strong>Sustainability of the pilots</strong><span>NAIRR is moving from pilot to at-scale. NRP is exploring sustained funding models. NSF is still reviewing proposals.</span></li>
</ol>

</NativeFrame>

---

<NativeFrame kicker="KEY TAKEAWAYS" title="Five things I'd like you to walk away with" page="17 / 19">

<div class="takeaways">
  <div><strong>NRP is real, free, and growing fast.</strong><span>129 sites · 1,532 GPUs · 5,800 users · 90% reach it through Jupyter. Cal Poly is already on it.</span></div>
  <div><strong>Kubernetes is the substrate; Jupyter is the front door.</strong><span>Most users never see K8s. The interesting thing is the notebook layer — and now the LLM service on top.</span></div>
  <div><strong>Research and education, side by side.</strong><span>The platform serves teaching and research at once.</span></div>
  <div><strong>California is central — and Cal Poly fits the profile.</strong><span>72% of LLM token usage is in CA. CENIC is the network. Sister CSUs are running their own playbooks today.</span></div>
  <div><strong>The boundary between research, education, and IT is dissolving.</strong><span>Digital assets in the classroom, AI tutors, federated data, agentic workflows — this work crosses every silo.</span></div>
</div>

</NativeFrame>

---

<NativeFrame kicker="RESOURCES" title="Where to learn more" page="18 / 19">

<div class="two-col resources-layout">
  <div class="resource-list">
    <h3>Platforms & access</h3>
    <b>nrp.ai</b><span>The platform itself — sign in, get a namespace, read the docs</span>
    <b>nrp.ai/llmtoken</b><span>Generate an LLM API token</span>
    <b>nationaldataplatform.org</b><span>NDP catalog, classrooms, federation docs</span>
    <b>nairrpilot.org</b><span>NAIRR resource request form (~6 week turnaround)</span>
  </div>
  <div class="resource-list">
    <h3>Communities & curricula</h3>
    <b>dash.nrp-nautilus.io</b><span>NRP user dashboard and Grafana metrics</span>
    <b>data8.org / data6 curriculum</b><span>Open intro data-science course, K-12 through CCC</span>
    <b>carpentries.org</b><span>Open data/computational skills training community</span>
    <b>scil.ucsd.edu</b><span>Societal Computing & Innovation Lab — wildfire, climate, etc.</span>
  </div>
</div>

<div class="contact-strip">Want to talk further? brianspo@calpoly.edu · Slides and notes available on request.</div>

</NativeFrame>

---

<NativeFrame dark :footer="false" bodyClass="cover-body">

<div class="cover-kicker">QUESTIONS</div>

# What's catching your attention?

<p class="cover-byline"><strong>Brian Spolarich</strong> · brianspo@calpoly.edu · ITS AI Community of Practice</p>

</NativeFrame>
