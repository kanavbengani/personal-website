#!/usr/bin/env python3
"""Generates index.html. Edit the DATA below and re-run: python3 build.py"""
import base64, json, os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ASSETS = os.path.join(HERE, "assets")

L = json.load(open(os.path.join(ASSETS, "logos.json"), encoding="utf-8"))

def load(name, fallback):
    p = os.path.join(HERE, name)
    if os.path.exists(p):
        try: return json.load(open(p, encoding="utf-8"))
        except Exception as err: print("  ! ignoring bad", name, err)
    return fallback

LAYOUT  = load("layout.json",  {"cards": {}, "arcs": {}})
CONTENT = load("content.json", {"hub": {}, "cards": {}})
PREVIEW = "data:image/jpeg;base64," + base64.b64encode(
    open(os.path.join(ASSETS, "resume_preview.jpg"), "rb").read()).decode()
PDF = "data:application/pdf;base64," + base64.b64encode(
    open(os.path.join(HERE, "Kanav_Bengani_Resume.pdf"), "rb").read()).decode()

M = "—"

# cat: experience | education | project | research
# Ordered most recent first within each category; that order drives the radius.
DATA = [
 dict(id="hubspot", cat="experience", logo="hubspot", now=True,
   name="HubSpot", role="Software Engineer", when="Dec 2025 " + M + " now", place="Cambridge, MA",
   pts=["Built <b>agentic search</b> to enhance discovery and conversion of Marketplace integrations using <b>MCP tools</b> and skills.",
        "Devised a platform with <b>80k+ users/week</b> with <b>Java</b> + React allowing marketing to customize Marketplace content."],
   stack="Java · React · MCP · Agents"),
 dict(id="capitalone", cat="experience", logo="capitalone",
   name="Capital One", role="Software Engineering Intern", when="Jun " + M + " Aug 2025", place="",
   pts=["Created a web app using <b>Flask</b> APIs and a React frontend that extracts image data with <b>85% accuracy</b> using <b>OCR</b>.",
        "Assessed image quality for over <b>100,000 documents/day</b> " + M + " government-issued IDs, W-2s, and bank statements."],
   stack="Flask · React · OCR · Python"),
 dict(id="klaviyo", cat="experience", logo="klaviyo",
   name="Klaviyo", role="Software Engineering Co-op", when="Jan " + M + " May 2025", place="Boston, MA",
   pts=["Optimized nightly segmentation jobs to be <b>7× faster</b> by ingesting <b>91%</b> less duplicate records per second.",
        "Utilized <b>Django</b> (backend), <b>ClickHouse</b> (sharded database), and <b>Kafka</b> (event streams) to process customer queries.",
        "Distributed deployment across <b>192 Kubernetes</b> pods and managed cluster configurations using <b>ZooKeeper</b>."],
   stack="Django · ClickHouse · Kafka · Kubernetes · ZooKeeper"),
 dict(id="fidelity", cat="experience", logo="fidelity",
   name="Fidelity Investments", role="Software Engineering Intern", when="Jun " + M + " Aug 2024", place="",
   pts=["Automated the archival of approximately <b>500</b> internal associate compliance alerts per day for auditing purposes.",
        "Used <b>Azure Functions</b> to create APIs that retrieve alert data, package into a PDF, and send to document storage."],
   stack="Azure Functions · Python · APIs"),
 dict(id="jnj", cat="experience", logo="jnj",
   name="Johnson &amp; Johnson", role="Data Science Co-op", when="Jan " + M + " May 2024", place="Titusville, NJ",
   pts=["Developed <b>71% accurate</b> <b>scikit-learn</b> models in <b>Python</b> to help reps identify patients unlikely to receive therapy.",
        "Compared clustering (k-means/hierarchical), random forest, and decision tree as possible solutions."],
   stack="scikit-learn · Python · Clustering"),

 dict(id="ballboy", cat="project", logo="ballboy", now=True,
   name="Ballboy", role="Fantasy tennis", when="May 2026 " + M + " now", place="",
   pts=["Founded a platform launched on <b>iOS</b> where a growing user base joins fantasy leagues following live tennis matches.",
        "Lead engineering to ensure a <b>low-latency, real-time</b> app using tools like <b>Redis</b>, Cloudflare, Supabase, and Render."],
   stack="React Native · Django · Redis · Supabase · Cloudflare",
   links=[("App Store", "https://apps.apple.com/app/ballboy-tennis/id6765790453"),
          ("GitHub", "https://github.com/kanavbengani/tennis_fantasy")]),
 dict(id="reddit", cat="project", logo="reddit",
   name="Reddit Sentiment Analysis", role="Agentic application", when="Nov 2024", place="",
   pts=["Fine-tuned an <b>LLM</b> that given a college-related query, constructs sentiment from the respective subreddit.",
        "Parsed and filtered context using <b>RAG</b> and a <b>BERT</b> classifier; derived sentiment using the Meta <b>Llama 3.1B</b> model."],
   stack="RAG · BERT · Llama 3.1B · PyTorch",
   links=[("GitHub", "https://github.com/zatchet/university-opinion-mining")]),
 dict(id="reversi", cat="project", logo="reversi",
   name="Reversi", role="Java video game", when="Nov 2023", place="",
   pts=["Architected a 2 player (human or AI w/ minimax algorithm) Go-like board game using <b>OOP</b> and <b>MVC</b> architecture."],
   stack="Java · Minimax · MVC",
   links=[("GitHub", "https://github.com/kanavbengani/Reversi")]),

 dict(id="factevo", cat="research", logo="northeastern",
   name="FactEvo Optimization", role="Evolutionary computing", when="Mar " + M + " Jun 2024", place="",
   pts=["Utilized natural-based <b>evolutionary computing</b> to solve a university course scheduling optimization problem.",
        "Ran <b>100,000 generations</b> for natural selection to result in a pareto-optimal, i.e. non-dominated set of solutions."],
   stack="Evolutionary computing · Python"),
 dict(id="shriners", cat="research", logo="shriners",
   name="Shriners Children's", role="Biomedical AI", when="2020 " + M + " 2022", place="",
   pts=["Improved surgical outcomes for cerebral palsy patients by developing an index with a predictive <b>autoencoder</b> model.",
        "<b>Published</b> in the Journal of Biomechanics and presented posters at the GCMAS and ORS conferences."],
   cite='Wang SJ, Tabashum T, Kruger KM, et al., <b>Bengani K</b>, Albert MV. “Creating an autoencoder single summary metric to assess gait quality to compare surgical outcomes in children with cerebral palsy: The Shriners Gait Index (SGI).” <i>Journal of Biomechanics</i> 168:112092, May 2024.',
   stack="Autoencoders · Python",
   links=[("Publication", "https://pubmed.ncbi.nlm.nih.gov/38669795/")]),

 dict(id="neu", cat="education", logo="northeastern",
   name="Northeastern University", role="B.S. Data Science, Minor in Mathematics", when="2022 " + M + " 2025", place="Boston, MA",
   courses=[("Systems", ["Algorithms","Object-Oriented Design","Database Design","Large-scale Storage/Retrieval"]),
            ("AI &amp; ML", ["Machine Learning","Artificial Intelligence","NLP","LLM-Engineered Systems"]),
            ("Math &amp; Viz", ["Discrete Structures","Linear Algebra","Statistics","Information Visualization"])]),
 dict(id="tams", cat="education", logo="tams",
   name="Texas Academy of Mathematics &amp; Science", role="Computer Science Track", when="2020 " + M + " 2022", place="Denton, TX",
   pts=["Early-college honors program: completed the final two years of high school as a full-time university student at the University of North Texas."]),
]

CATS = [("experience","Work"),("project","Projects"),
        ("research","Research"),("education","Education")]
# Where each category sits around the dial (separate from legend order).
SECTOR_ORDER = ["experience","education","research","project"]
# keyboard shortcut per category, in legend order
KEYS = {"experience":"w","project":"a","research":"s","education":"d"}
# Which entry sits in which slot around the dial, following SECTOR_ORDER.
# Slot geometry still comes from the category counts; a card may sit in another
# category's arc, and keeps its own colour.
ORDER = ["ballboy","hubspot","capitalone","klaviyo","fidelity","jnj",
         "neu","tams","factevo","shriners","reversi","reddit"]

def js_entries():
    out=[]
    for e in DATA:
        d={k:e[k] for k in ("id","cat","name","role","when") }
        d["logo"]=e["logo"]
        if e.get("now"): d["now"]=1
        if e.get("place"): d["place"]=e["place"]
        if e.get("pts"): d["pts"]=e["pts"]
        if e.get("stack"): d["stack"]=e["stack"]
        if e.get("cite"): d["cite"]=e["cite"]
        if e.get("links"): d["links"]=e["links"]
        if e.get("courses"): d["courses"]=e["courses"]
        out.append(d)
    return json.dumps(out, ensure_ascii=True, separators=(",",":"))

HTML = """<meta charset="utf-8">
<title>Kanav Bengani</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,600;12..96,700&family=Newsreader:ital,opsz,wght@0,6..72,300;0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,300&family=JetBrains+Mono:wght@400;500;700&display=swap">
<script src="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.min.js"></script>

<style>
:root{
  --paper:#F6F4F7; --panel:#FFFFFF; --ink:#17131C; --ink-2:#4E4757; --muted:#8B8394;
  --line:#DFD9E3; --hair:#EAE5EE; --hover:#EFEBF2; --wire:#D8D1DD;
  --tile:#FFFFFF; --tile-line:#E4DEE8; --scrim:rgba(23,19,28,.34);
  --c-experience:#8E4B6E; --c-project:#3C7A78; --c-research:#8A6A35; --c-education:#4E5B86;
  --bg-experience:#FBF3F7; --bd-experience:#E9D6E0;
  --bg-project:#EFF7F6;    --bd-project:#CEE4E1;
  --bg-research:#FBF6EC;   --bd-research:#EADEC6;
  --bg-education:#F2F4FB;  --bd-education:#D7DDEE;
  --a-experience:#6B2A4C; --a-project:#1F5250; --a-research:#66491A; --a-education:#2E3B67;
  color-scheme:light;
}
:root[data-theme="dark"]{
  --paper:#111016; --panel:#191721; --ink:#EDEAF0; --ink-2:#A9A1B2; --muted:#7A7183;
  --line:#262230; --hair:#1D1A24; --hover:#1C1926; --wire:#2A2534;
  --tile:#F2EFF4; --tile-line:#2B2734; --scrim:rgba(0,0,0,.62);
  --c-experience:#D98BB0; --c-project:#6FCFC7; --c-research:#D2A857; --c-education:#94A6DC;
  --bg-experience:#241A21; --bd-experience:#3E2C36;
  --bg-project:#152220;    --bd-project:#243B38;
  --bg-research:#221E14;   --bd-research:#3B3323;
  --bg-education:#181C27;  --bd-education:#2A3147;
  --a-experience:#EFA0C0; --a-project:#84DDD5; --a-research:#E0B96A; --a-education:#A8B7E6;
  color-scheme:dark;
}
*{box-sizing:border-box}
[hidden]{display:none !important}
body{margin:0;background:var(--paper);color:var(--ink);
  font-family:"Newsreader",Georgia,"Times New Roman",serif;font-size:15px;line-height:1.5;
  -webkit-font-smoothing:antialiased}
::selection{background:var(--ink);color:var(--paper)}
:focus-visible{outline:1px solid var(--ink);outline-offset:3px;border-radius:4px}
a{color:inherit}
.sr{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0 0 0 0);white-space:nowrap}

/* ---------- top bar ---------- */


/* ---------- stage ---------- */
.stage{position:relative;width:100%;height:100vh;min-height:680px;overflow:hidden}
.wires{position:absolute;inset:0;width:100%;height:100%;pointer-events:none;z-index:0}
.wires line{stroke:var(--wire);stroke-width:1;transition:opacity .3s,stroke .3s}

.hub{position:absolute;left:50%;top:50%;transform:translate(-50%,-50%);
  width:min(468px,80vw);text-align:center;z-index:2;pointer-events:none;
  background:var(--panel);border:1px solid var(--hair);border-radius:16px;
  padding:50px 34px 52px;box-shadow:0 2px 24px rgba(0,0,0,.05)}
.corners{display:contents}
.hub .ico{position:absolute;pointer-events:auto;
  display:inline-flex;align-items:center;justify-content:center;
  width:38px;height:38px;border-radius:10px;color:var(--muted);
  background:none;border:1px solid transparent;padding:0;cursor:pointer;text-decoration:none;
  transition:color .16s,background .16s,border-color .16s}
.hub .ico:hover{color:var(--ink);background:var(--hover);border-color:var(--line)}
.hub .ico svg{width:23px;height:23px;display:block}
.hub .ico.tl{top:11px;left:11px}
.hub .ico.tr{top:11px;right:11px}
.hub .ico.bl{bottom:11px;left:11px}
.hub .ico.br{bottom:11px;right:11px}
.hub .ico .lab{position:absolute;top:calc(100% + 6px);left:50%;transform:translateX(-50%);
  background:var(--panel);border:1px solid var(--line);border-radius:5px;padding:4px 8px;
  font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--ink-2);white-space:nowrap;pointer-events:none;
  opacity:0;visibility:hidden;transition:opacity .15s,visibility .15s;z-index:9}
.hub .ico.bl .lab,.hub .ico.br .lab{top:auto;bottom:calc(100% + 6px)}
.hub .ico:hover .lab,.hub .ico:focus-visible .lab{opacity:1;visibility:visible}
.hub h1{font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;font-weight:600;
  font-size:clamp(30px,4.6vw,46px);letter-spacing:-.034em;line-height:1;margin:0}
.hub .role-line{margin:11px 0 0;font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;
  font-weight:600;font-size:12px;letter-spacing:.15em;text-transform:uppercase;color:var(--muted);
  pointer-events:auto}
.hub .role-line .tip{color:var(--ink)}
.hub p.bio{margin:13px auto 0;max-width:37ch;color:var(--ink-2);font-weight:500;font-size:15.5px;
  line-height:1.5;text-wrap:balance;pointer-events:auto}
.hub em{font-style:italic;color:var(--ink)}
.tip{position:relative;text-decoration:none;border-bottom:1px dotted var(--muted)}
.tip:hover{border-bottom-color:var(--ink)}
.tipbox{position:absolute;left:50%;bottom:calc(100% + 8px);transform:translateX(-50%);
  background:var(--panel);border:1px solid var(--line);border-radius:5px;padding:5px 9px;
  white-space:nowrap;pointer-events:none;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;
  font-size:9px;letter-spacing:.07em;text-transform:uppercase;font-style:normal;color:var(--ink-2);
  opacity:0;visibility:hidden;transition:opacity .15s;z-index:9}
.tip:hover .tipbox,.tip:focus-visible .tipbox{opacity:1;visibility:visible}

/* ---------- cards ---------- */
.card{position:absolute;z-index:3;width:238px;
  background:var(--panel);border:1px solid var(--line);border-radius:9px;
  padding:11px 13px;cursor:pointer;text-align:left;color:inherit;font:inherit;
  display:grid;grid-template-columns:22px 1fr;gap:0 10px;align-items:center;
  box-shadow:0 1px 2px rgba(0,0,0,.03);
  transition:transform .22s cubic-bezier(.2,.7,.3,1),box-shadow .22s,border-color .18s,opacity .3s}
.card:hover,.card:focus-visible{box-shadow:0 10px 26px rgba(0,0,0,.12);border-color:var(--muted);z-index:5}
.card .mark{width:22px;height:22px;border-radius:5px;overflow:hidden;
  background:var(--tile);border:1px solid var(--tile-line);display:flex;align-items:center;justify-content:center}
.card .mark img{width:100%;height:100%;object-fit:contain;display:block}
.card .nm{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:13.5px;
  letter-spacing:-.016em;line-height:1.2;display:block}
.card .rl{font-style:italic;font-weight:300;color:var(--muted);font-size:11.5px;
  line-height:1.3;display:block;margin-top:1px}
.card .meta{grid-column:2;display:flex;align-items:center;gap:7px;margin-top:5px}
.card .dot{width:5px;height:5px;border-radius:50%;flex:none}
.card .wh{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9px;
  color:var(--muted);letter-spacing:.04em;font-variant-numeric:tabular-nums}
.card .live{margin-left:auto;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;
  font-size:8px;letter-spacing:.12em;text-transform:uppercase;color:var(--paper);
  background:var(--ink);border-radius:99px;padding:2px 6px}
.card[data-cat="experience"]{background:var(--bg-experience);border-color:var(--bd-experience)}
.card[data-cat="project"]{background:var(--bg-project);border-color:var(--bd-project)}
.card[data-cat="research"]{background:var(--bg-research);border-color:var(--bd-research)}
.card[data-cat="education"]{background:var(--bg-education);border-color:var(--bd-education)}
.card[data-cat="experience"] .dot{background:var(--c-experience)}
.card[data-cat="project"] .dot{background:var(--c-project)}
.card[data-cat="research"] .dot{background:var(--c-research)}
.card[data-cat="education"] .dot{background:var(--c-education)}
.card .live{background:var(--c-experience)}
.card[data-cat="project"] .live{background:var(--c-project)}
.card.now{box-shadow:0 0 0 1px var(--ink) inset,0 1px 2px rgba(0,0,0,.03)}
.stage.filtered .card:not(.on){opacity:.26;filter:grayscale(1)}
.stage.filtered .card.on{box-shadow:0 6px 18px rgba(0,0,0,.10)}

/* link tooltip on a card */
.ltip{position:absolute;z-index:7;left:50%;bottom:calc(100% + 8px);transform:translateX(-50%) translateY(4px);
  display:flex;gap:6px;background:var(--panel);border:1px solid var(--line);border-radius:7px;
  padding:6px;white-space:nowrap;box-shadow:0 8px 22px rgba(0,0,0,.13);
  opacity:0;visibility:hidden;transition:opacity .16s,transform .16s,visibility .16s}
.card:hover .ltip,.card:focus-within .ltip{opacity:1;visibility:visible;transform:translateX(-50%) translateY(0)}
.ltip a{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9.5px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--ink-2);text-decoration:none;border:1px solid var(--line);
  border-radius:5px;padding:5px 9px;transition:background .15s,color .15s,border-color .15s}
.ltip a:hover{background:var(--hover);color:var(--ink);border-color:var(--muted)}
.ltip::after{content:"";position:absolute;top:100%;left:50%;margin-left:-5px;
  border:5px solid transparent;border-top-color:var(--line)}

/* ---------- arc labels ---------- */
.arcs{position:absolute;inset:0;pointer-events:none;z-index:1}
.arc{position:absolute;transform-origin:50% 50%;white-space:nowrap;
  font-family:"Bricolage Grotesque","Helvetica Neue",Arial,sans-serif;font-weight:700;
  font-size:16px;letter-spacing:.09em;text-transform:uppercase;
  opacity:1;transition:opacity .25s}
body.editing .arcs{pointer-events:auto}
body.editing .arc{cursor:move;opacity:1;outline:1px dashed var(--line);outline-offset:6px}
.arc-h{display:none;position:absolute;right:-22px;top:50%;margin-top:-6px;
  width:12px;height:12px;border-radius:50%;background:var(--panel);
  border:1px solid var(--muted);cursor:grab}
body.editing .arc-h{display:block}
.stage.filtered .arc{opacity:.22}
.stage.filtered .arc.on{opacity:1}
.arc[data-cat="experience"]{color:var(--a-experience)}
.arc[data-cat="project"]{color:var(--a-project)}
.arc[data-cat="research"]{color:var(--a-research)}
.arc[data-cat="education"]{color:var(--a-education)}

/* ---------- local editor ---------- */
.editbar{position:fixed;left:20px;bottom:20px;z-index:40;display:none;align-items:center;gap:8px;
  background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:8px 10px;
  box-shadow:0 8px 26px rgba(0,0,0,.14)}
body.has-editor .editbar{display:flex}
.editbar button{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;
  font-weight:700;letter-spacing:.08em;text-transform:uppercase;cursor:pointer;
  background:none;color:var(--ink-2);border:1px solid var(--line);border-radius:5px;padding:6px 10px;
  transition:background .15s,color .15s,border-color .15s}
.editbar button:hover{background:var(--hover);color:var(--ink);border-color:var(--muted)}
.editbar button.primary{background:var(--ink);color:var(--paper);border-color:var(--ink)}
.editbar button.primary:hover{opacity:.86;background:var(--ink);color:var(--paper)}
.editbar .st{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9.5px;
  color:var(--muted);letter-spacing:.05em;min-width:96px}

body.editing .card{cursor:move;user-select:none}
body.editing .card:hover{box-shadow:0 0 0 1px var(--c-experience),0 10px 26px rgba(0,0,0,.12)}
body.editing .ltip{display:none}
.handle{position:absolute;width:11px;height:11px;border-radius:50%;background:var(--panel);
  border:1px solid var(--muted);display:none;z-index:8}
body.editing .card .handle{display:block}
.h-w{right:-6px;top:50%;margin-top:-5.5px;cursor:ew-resize;border-radius:2px}
.h-r{left:50%;top:-17px;margin-left:-5.5px;cursor:grab}
.editbtn{position:absolute;right:-10px;top:-10px;display:none;z-index:9;
  width:22px;height:22px;border-radius:50%;cursor:pointer;line-height:1;
  background:var(--panel);border:1px solid var(--muted);color:var(--ink-2);font-size:11px}
body.editing .card .editbtn{display:block}
.editbtn:hover{background:var(--ink);color:var(--paper);border-color:var(--ink)}

/* editable modal */
.ed-row{margin-top:12px}
.ed-lab{display:block;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9px;
  letter-spacing:.13em;text-transform:uppercase;color:var(--muted);margin-bottom:5px}
.ed-box{border:1px solid var(--line);border-radius:6px;padding:8px 10px;min-height:20px;
  color:var(--ink-2);font-size:15px;line-height:1.5;background:var(--paper)}
.ed-box:focus{outline:none;border-color:var(--ink)}
.ed-list{display:flex;flex-direction:column;gap:7px}
.ed-item{display:flex;gap:7px;align-items:flex-start}
.ed-item .ed-box{flex:1}
.ed-x{flex:none;background:none;border:1px solid var(--line);border-radius:5px;cursor:pointer;
  color:var(--muted);width:26px;height:26px;line-height:1;font-size:13px;margin-top:3px}
.ed-x:hover{color:var(--ink);border-color:var(--muted)}
.ed-add{margin-top:7px;background:none;border:1px dashed var(--line);border-radius:5px;cursor:pointer;
  color:var(--muted);font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9.5px;
  letter-spacing:.08em;text-transform:uppercase;padding:6px 10px}
.ed-add:hover{color:var(--ink);border-color:var(--muted)}
.ed-in{flex:1;min-width:0;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:11px;
  background:var(--paper);color:var(--ink);border:1px solid var(--line);border-radius:6px;padding:7px 9px}
.ed-in:focus{outline:none;border-color:var(--ink)}
.ed-foot{margin-top:18px;padding-top:14px;border-top:1px solid var(--hair);display:flex;gap:10px;align-items:center}
.ed-apply{background:var(--ink);color:var(--paper);border:1px solid var(--ink);border-radius:5px;
  cursor:pointer;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;
  font-weight:700;letter-spacing:.08em;text-transform:uppercase;padding:8px 14px}
.ed-hint{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9.5px;color:var(--muted)}
.card [contenteditable]{outline:none}
body.editing .card [contenteditable]:hover,
body.editing .hub [contenteditable]:hover{box-shadow:inset 0 -1px 0 var(--muted)}
body.editing [contenteditable]:focus{box-shadow:inset 0 -1px 0 var(--ink) !important}

/* ---------- legend ---------- */
.legend{position:absolute;right:26px;bottom:24px;z-index:6;
  background:var(--panel);border:1px solid var(--line);border-radius:9px;padding:12px 13px;
  box-shadow:0 6px 20px rgba(0,0,0,.07);min-width:158px}
.legend h2{margin:0 0 9px;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;
  font-size:8.5px;letter-spacing:.19em;text-transform:uppercase;color:var(--muted)}
.legend button{display:flex;align-items:center;gap:8px;width:100%;background:none;border:0;
  padding:5px 6px;margin:0 -6px;border-radius:5px;cursor:pointer;color:var(--ink-2);
  font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.06em;
  text-transform:uppercase;text-align:left;transition:background .15s,color .15s}
.legend button:hover{background:var(--hover);color:var(--ink)}
.legend button[aria-pressed="true"]{background:var(--hover);color:var(--ink)}
.legend .sw{width:8px;height:8px;border-radius:50%;flex:none}
.legend .clear{justify-content:center;margin-top:7px;padding-top:9px;border-top:1px solid var(--hair);
  border-radius:0;color:var(--muted)}
.legend kbd{margin-left:auto;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:8.5px;
  border:1px solid var(--line);border-radius:3px;padding:1px 4px;color:var(--muted);
  min-width:15px;text-align:center}
.legend button[aria-pressed="true"] kbd{border-color:var(--muted);color:var(--ink)}

/* ---------- mobile list ---------- */
.list{display:none;max-width:640px;margin:0 auto;padding:8px 26px 48px}
.list h2{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-weight:400;font-size:9.5px;
  letter-spacing:.18em;text-transform:uppercase;color:var(--muted);
  margin:26px 0 0;padding-bottom:8px;border-bottom:1px solid var(--line)}
.list ul{list-style:none;margin:0;padding:0}
.rw{position:relative;display:grid;grid-template-columns:24px 1fr auto;align-items:center;gap:0 13px;
  padding:11px 8px;margin:0 -8px;border-radius:5px}
.rw + .rw{box-shadow:0 -1px 0 var(--hair)}
.rw .hit{position:absolute;inset:0;background:none;border:0;cursor:pointer;border-radius:5px;
  transition:background .14s;z-index:0}
.rw .hit:hover{background:var(--hover)}
.rw > *:not(.hit){position:relative;z-index:1;pointer-events:none}
.rw .mark{width:24px;height:24px;border-radius:5px;overflow:hidden;background:var(--tile);
  border:1px solid var(--tile-line);display:flex;align-items:center;justify-content:center}
.rw .mark img{width:100%;height:100%;object-fit:contain;display:block}
.rw .nm{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:15px;letter-spacing:-.016em;display:block}
.rw .rl{font-style:italic;font-weight:300;color:var(--muted);font-size:13px;display:block;margin-top:1px}
.rw .rlinks{display:flex;gap:12px;margin-top:5px;pointer-events:auto}
.rw .rlinks a{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9.5px;
  letter-spacing:.08em;text-transform:uppercase;color:var(--muted);text-decoration:none;
  border-bottom:1px solid var(--line);padding-bottom:1px}
.rw .rlinks a:hover{color:var(--ink);border-bottom-color:var(--ink)}
.rw .wh{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;color:var(--muted);
  white-space:nowrap;font-variant-numeric:tabular-nums}

/* List mode: the hard breakpoint sets it before paint, and layout() also
   turns it on the moment the cards can no longer be placed without touching. */
:root.list-mode .stage{height:auto;min-height:0;overflow:visible;padding:26px 0 6px}
:root.list-mode .wires,
:root.list-mode .legend,
:root.list-mode .arcs{display:none}
:root.list-mode .hub{position:static;transform:none;width:auto;margin:0 auto;padding:0 26px;
  background:none;border:0;box-shadow:none}
:root.list-mode .corners{display:flex;justify-content:center;gap:4px;margin-top:18px}
:root.list-mode .hub .ico{position:static}
:root.list-mode .hub .ico .lab{display:none}
:root.list-mode .card{display:none}
:root.list-mode .list{display:block}

/* ---------- modals ---------- */
dialog{border:0;padding:0;background:transparent;color:var(--ink);
  max-width:min(520px,calc(100vw - 32px));width:100%}
dialog::backdrop{background:var(--scrim)}
.panel{background:var(--panel);border:1px solid var(--line);border-radius:10px;
  padding:26px 26px 24px;position:relative;box-shadow:0 14px 40px rgba(0,0,0,.14);
  max-height:calc(100vh - 64px);overflow-y:auto}
.close{position:absolute;top:14px;right:14px;background:none;border:0;cursor:pointer;
  font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.08em;
  text-transform:uppercase;color:var(--muted);padding:4px 6px;border-radius:4px;transition:color .16s}
.close:hover{color:var(--ink)}
.d-head{display:flex;align-items:center;gap:12px;padding-right:44px}
.d-head .mark{width:38px;height:38px;border-radius:8px;overflow:hidden;background:var(--tile);
  border:1px solid var(--tile-line);display:flex;align-items:center;justify-content:center;flex:none}
.d-head .mark img{width:100%;height:100%;object-fit:contain;display:block}
.d-name{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:20px;
  letter-spacing:-.02em;line-height:1.2;display:block}
.d-role{font-style:italic;font-weight:300;color:var(--muted);font-size:14.5px;display:block;margin-top:2px}
.d-meta{margin:14px 0 0;padding-bottom:14px;border-bottom:1px solid var(--hair);
  font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--muted);display:flex;gap:14px;flex-wrap:wrap;align-items:center}
.d-meta .dot{width:6px;height:6px;border-radius:50%}
.d-pts{margin:14px 0 0;padding:0;list-style:none;display:flex;flex-direction:column;gap:9px}
.d-pts li{position:relative;padding-left:16px;color:var(--ink-2);font-size:15.5px;line-height:1.55}
.d-pts li::before{content:"";position:absolute;left:0;top:.72em;width:7px;height:1px;background:var(--muted)}
.d-pts b{color:var(--ink);font-weight:600;font-variant-numeric:tabular-nums}
.courses{margin-top:16px;display:flex;flex-direction:column;gap:12px}
.cgroup{display:grid;grid-template-columns:74px 1fr;gap:10px;align-items:baseline}
.clabel{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:9px;letter-spacing:.13em;
  text-transform:uppercase;color:var(--muted);padding-top:4px}
.cchips{display:flex;flex-wrap:wrap;gap:5px}
.chip{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;color:var(--ink-2);
  border:1px solid var(--line);border-radius:4px;padding:3px 7px;line-height:1.4}
@media (max-width:420px){.cgroup{grid-template-columns:1fr;gap:4px}}
.cite{margin:14px 0 0;padding:12px 14px;background:var(--paper);border-radius:6px;
  color:var(--ink-2);font-size:13.5px;line-height:1.5}
.cite b{color:var(--ink);font-weight:600}
.d-stack{margin:16px 0 0;font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;
  letter-spacing:.05em;color:var(--muted);line-height:1.8}
.d-links{margin:16px 0 0;display:flex;flex-wrap:wrap;gap:16px}
.d-links a{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10.5px;letter-spacing:.06em;
  text-transform:uppercase;color:var(--muted);text-decoration:none;border-bottom:1px solid var(--line);
  padding-bottom:2px;transition:color .16s,border-color .16s}
.d-links a:hover{color:var(--ink);border-bottom-color:var(--ink)}
dialog[open]{animation:pop .18s cubic-bezier(.2,.7,.3,1)}
@keyframes pop{from{opacity:0;transform:translateY(6px)}to{opacity:1;transform:none}}

#resumeDlg{max-width:min(820px,calc(100vw - 32px))}
#resumeDlg .panel{padding:22px 22px 20px}
.r-head{display:flex;align-items:baseline;justify-content:space-between;gap:16px;flex-wrap:wrap;
  padding-right:56px;padding-bottom:14px;border-bottom:1px solid var(--hair)}
.r-name{font-family:"Bricolage Grotesque",sans-serif;font-weight:600;font-size:19px;letter-spacing:-.02em}
.r-sub{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.07em;
  text-transform:uppercase;color:var(--muted)}
.r-frame{margin-top:16px;border:1px solid var(--line);border-radius:6px;overflow:hidden;
  background:#FFFFFF;line-height:0;max-height:64vh;overflow-y:auto}
.r-frame img,.r-frame canvas{width:100%;height:auto;display:block}
.r-actions{margin-top:16px;display:flex;flex-wrap:wrap;gap:10px 12px;align-items:center}
.r-btn{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10.5px;letter-spacing:.08em;
  text-transform:uppercase;text-decoration:none;color:var(--ink);border:1px solid var(--line);
  border-radius:5px;padding:8px 14px;transition:border-color .16s,background .16s}
.r-btn:hover{border-color:var(--ink);background:var(--hover)}
.r-btn.ghost{color:var(--muted);border-color:transparent}
.r-btn.ghost:hover{color:var(--ink);border-color:var(--line)}
.r-note{font-family:"JetBrains Mono",ui-monospace,Menlo,monospace;font-size:10px;color:var(--muted)}

@media (prefers-reduced-motion:reduce){
  *{animation:none !important}
  .card{transition:opacity .2s,border-color .2s}
}
</style>


<script>
/* before first paint, so a small window never flashes the graph */
(function(){var r=document.documentElement;
 if(window.innerWidth<=900||window.innerHeight<=600) r.classList.add("list-mode");})();
</script>

<main class="stage" id="stage">
  <svg class="wires" id="wires" aria-hidden="true"></svg>
  <div class="hub">
    <h1>Kanav Bengani</h1>
    <p class="role-line">Software Engineer @ <a class="tip" href="#hubspot" data-card="hubspot">HubSpot<span class="tipbox">See the HubSpot card</span></a></p>
    <p class="bio">I like building backend systems, tinkering with the buzzword that is AI,
      and occasionally making things people actually use &mdash;
      like <a class="tip" href="#ballboy" data-card="ballboy"><em>Ballboy</em><span class="tipbox">See the Ballboy card</span></a>.</p>
  <div class="corners">
    <a class="ico tl" href="https://github.com/kanavbengani" target="_blank" rel="noopener" aria-label="GitHub"><svg viewBox="0 0 16 16" fill="currentColor" aria-hidden="true"><path d="M8 0C3.58 0 0 3.58 0 8c0 3.54 2.29 6.53 5.47 7.59.4.07.55-.17.55-.38 0-.19-.01-.82-.01-1.49-2.01.37-2.53-.49-2.69-.94-.09-.23-.48-.94-.82-1.13-.28-.15-.68-.52-.01-.53.63-.01 1.08.58 1.23.82.72 1.21 1.87.87 2.33.66.07-.52.28-.87.51-1.07-1.78-.2-3.64-.89-3.64-3.95 0-.87.31-1.59.82-2.15-.08-.2-.36-1.02.08-2.12 0 0 .67-.21 2.2.82.64-.18 1.32-.27 2-.27s1.36.09 2 .27c1.53-1.04 2.2-.82 2.2-.82.44 1.1.16 1.92.08 2.12.51.56.82 1.27.82 2.15 0 3.07-1.87 3.75-3.65 3.95.29.25.54.73.54 1.48 0 1.07-.01 1.93-.01 2.2 0 .21.15.46.55.38A8.01 8.01 0 0 0 16 8c0-4.42-3.58-8-8-8z"/></svg><span class="lab">GitHub</span></a>
    <a class="ico tr" href="https://linkedin.com/in/kanavbengani" target="_blank" rel="noopener" aria-label="LinkedIn"><svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M20.45 20.45h-3.56v-5.57c0-1.33-.03-3.04-1.85-3.04-1.85 0-2.13 1.45-2.13 2.94v5.67H9.35V9h3.41v1.56h.05c.48-.9 1.64-1.85 3.37-1.853.6 0 4.27 2.37 4.27 5.45v6.29zM5.34 7.43a2.06 2.06 0 1 1 0-4.13 2.06 2.06 0 0 1 0 4.13zM7.12 20.45H3.56V9h3.56v11.45zM22.22 0H1.77C.79 0 0 .77 0 1.72v20.56C0 23.23.79 24 1.77 24h20.45c.98 0 1.78-.77 1.78-1.72V1.72C24 .77 23.2 0 22.22 0z"/></svg><span class="lab">LinkedIn</span></a>
    <button class="ico bl" id="resumeBtn" type="button" aria-label="Resume"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M14 3H7a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h10a2 2 0 0 0 2-2V8z"/><path d="M14 3v5h5"/><path d="M9 13h6"/><path d="M9 17h4"/></svg><span class="lab">Resume</span></button>
    <button class="ico br" id="themeBtn" type="button" aria-label="Toggle theme"><svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.7"/><path d="M12 3a9 9 0 0 1 0 18z" fill="currentColor"/></svg><span class="lab">Theme</span></button>
  </div>
  </div>
  <div class="arcs" id="arcs" aria-hidden="true"></div>
  <div id="cards"></div>
  <nav class="legend" id="legend" aria-label="Filter by category"><h2>Legend</h2></nav>
</main>

<div class="list" id="list"></div>

<dialog id="dlg"><div class="panel">
  <button class="close" type="button" id="closeBtn" aria-label="Close">Close</button>
  <div id="dlgBody"></div>
</div></dialog>

<dialog id="resumeDlg"><div class="panel">
  <button class="close" type="button" id="resumeClose" aria-label="Close">Close</button>
  <div class="r-head"><span class="r-name">Resume</span>
    <span class="r-sub">PDF &middot; 1 page &middot; updated 2026</span></div>
  <div class="r-frame">
    <canvas id="pdfCanvas" hidden aria-label="Page 1 of the resume"></canvas>
    <img id="pdfImg" src="__PREVIEW__" alt="Preview of Kanav Bengani's resume">
  </div>
  <div class="r-actions">
    <a class="r-btn" id="dlBtn" href="__PDF__" download="Kanav_Bengani_Resume.pdf">Download PDF</a>
    <a class="r-btn ghost" id="openBtn" href="Kanav_Bengani_Resume.pdf" target="_blank" rel="noopener">Open in new tab &#8599;</a>
    <span class="r-note" id="dlNote" role="status"></span>
  </div>
</div></dialog>

<script>
var LOGOS = __LOGOS__;
var ENTRIES = __ENTRIES__;
var CATS = __CATS__;
var SECTOR_ORDER = __SECTORS__;
var KEYS = __KEYS__;
var ORDER = __ORDER__;
var LAYOUT = __LAYOUT__;
var CONTENT = __CONTENT__;
var LOCAL = ["localhost","127.0.0.1","::1"].indexOf(location.hostname)>=0;
</script>
<script>
(function(){
"use strict";
var reduce = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
var editing = false;
var root = document.documentElement;

/* ---------------- theme ---------------- */
var themeBtn = document.getElementById("themeBtn");
function curTheme(){ return root.getAttribute("data-theme")==="dark" ? "dark" : "light"; }
try{ if(localStorage.getItem("kb-theme")==="dark") root.setAttribute("data-theme","dark"); }catch(e){}
themeBtn.addEventListener("click",function(){
  var n = curTheme()==="dark" ? "light" : "dark";
  root.setAttribute("data-theme", n);
  try{ localStorage.setItem("kb-theme", n); }catch(e){}
});

/* ---------------- detail modal ---------------- */
var dlg=document.getElementById("dlg"), dlgBody=document.getElementById("dlgBody"), lastFocus=null;
function esc(s){ return s; }
function detailHTML(e){
  var h='<div class="d-head"><span class="mark"><img src="'+LOGOS[e.logo]+'" alt=""></span>'+
        '<span><span class="d-name">'+e.name+'</span><span class="d-role">'+e.role+'</span></span></div>';
  h+='<p class="d-meta"><span class="dot" style="background:var(--c-'+e.cat+')"></span>'+
     '<span>'+catLabel(e.cat)+'</span><span>'+e.when+'</span>'+(e.place?'<span>'+e.place+'</span>':'')+'</p>';
  if(e.pts){ h+='<ul class="d-pts">'; for(var i=0;i<e.pts.length;i++) h+='<li>'+e.pts[i]+'</li>'; h+='</ul>'; }
  if(e.courses){
    h+='<div class="courses">';
    for(var j=0;j<e.courses.length;j++){
      h+='<div class="cgroup"><span class="clabel">'+e.courses[j][0]+'</span><span class="cchips">';
      var cs=e.courses[j][1];
      for(var k=0;k<cs.length;k++) h+='<span class="chip">'+cs[k]+'</span>';
      h+='</span></div>';
    }
    h+='</div>';
  }
  if(e.cite) h+='<p class="cite">'+e.cite+'</p>';
  if(e.stack) h+='<p class="d-stack">'+e.stack+'</p>';
  if(e.links){
    h+='<p class="d-links">';
    for(var m=0;m<e.links.length;m++) h+='<a href="'+e.links[m][1]+'" target="_blank" rel="noopener">'+e.links[m][0]+' &#8599;</a>';
    h+='</p>';
  }
  return h;
}
function esc2(t){ return String(t==null?"":t).replace(/&/g,"&amp;").replace(/</g,"&lt;").replace(/"/g,"&quot;"); }
function editHTML(e){
  var h='<div class="d-head"><span class="mark"><img src="'+LOGOS[e.logo]+'" alt=""></span>'+
        '<span><span class="d-name" id="ed-echo">'+e.name+'</span>'+
        '<span class="d-role">Editing this card</span></span></div>';
  h+='<div class="ed-row"><span class="ed-lab">Title</span>'+
     '<div class="ed-box" id="ed-name" contenteditable="true">'+e.name+'</div></div>';
  h+='<div class="ed-row"><span class="ed-lab">Subtitle</span>'+
     '<div class="ed-box" id="ed-role" contenteditable="true">'+e.role+'</div></div>';
  h+='<div class="ed-row"><span class="ed-lab">Date</span>'+
     '<div class="ed-box" id="ed-when" contenteditable="true">'+e.when+'</div></div>';
  h+='<div class="ed-row"><span class="ed-lab">Location</span>'+
     '<div class="ed-box" id="ed-place" contenteditable="true">'+(e.place||"")+'</div></div>';
  h+='<div class="ed-row"><span class="ed-lab">Bullets</span><div class="ed-list" id="ed-pts">';
  (e.pts||[]).forEach(function(p){
    h+='<div class="ed-item"><div class="ed-box" contenteditable="true">'+p+'</div>'+
       '<button class="ed-x" type="button" data-x="pt">&times;</button></div>';
  });
  h+='</div><button class="ed-add" type="button" id="ed-addpt">+ bullet</button></div>';
  h+='<div class="ed-row"><span class="ed-lab">Stack</span>'+
     '<div class="ed-box" id="ed-stack" contenteditable="true">'+(e.stack||"")+'</div></div>';
  h+='<div class="ed-row"><span class="ed-lab">Links</span><div class="ed-list" id="ed-links">';
  (e.links||[]).forEach(function(l){
    h+='<div class="ed-item"><input class="ed-in" data-k="label" value="'+esc2(l[0])+'" placeholder="Label">'+
       '<input class="ed-in" data-k="url" value="'+esc2(l[1])+'" placeholder="https://">'+
       '<button class="ed-x" type="button" data-x="link">&times;</button></div>';
  });
  h+='</div><button class="ed-add" type="button" id="ed-addlink">+ link</button></div>';
  h+='<div class="ed-row"><span class="ed-lab">Citation (optional)</span>'+
     '<div class="ed-box" id="ed-cite" contenteditable="true">'+(e.cite||"")+'</div></div>';
  h+='<div class="ed-foot"><button class="ed-apply" type="button" id="ed-apply">Apply</button>'+
     '<span class="ed-hint">then Save to write content.json</span></div>';
  return h;
}
function catLabel(c){ for(var i=0;i<CATS.length;i++) if(CATS[i][0]===c) return CATS[i][1]; return c; }
function openDetail(id, origin, asEdit){
  var e=byId(id); if(!e) return;
  lastFocus=origin||null;
  dlgBody.innerHTML=asEdit?editHTML(e):detailHTML(e);
  if(asEdit) wireEditor(e);
  if(dlg.showModal) dlg.showModal(); else dlg.setAttribute("open","");
}
function wireEditor(e){
  var pts=dlgBody.querySelector("#ed-pts"), links=dlgBody.querySelector("#ed-links");
  var nameBox=dlgBody.querySelector("#ed-name"), echo=dlgBody.querySelector("#ed-echo");
  nameBox.addEventListener("input",function(){ echo.innerHTML=nameBox.innerHTML; });
  dlgBody.querySelector("#ed-addpt").addEventListener("click",function(){
    var d=document.createElement("div");
    d.className="ed-item";
    d.innerHTML='<div class="ed-box" contenteditable="true"></div><button class="ed-x" type="button" data-x="pt">&times;</button>';
    pts.appendChild(d); d.firstChild.focus();
  });
  dlgBody.querySelector("#ed-addlink").addEventListener("click",function(){
    var d=document.createElement("div");
    d.className="ed-item";
    d.innerHTML='<input class="ed-in" data-k="label" placeholder="Label">'+
                '<input class="ed-in" data-k="url" placeholder="https://">'+
                '<button class="ed-x" type="button" data-x="link">&times;</button>';
    links.appendChild(d); d.firstChild.focus();
  });
  dlgBody.addEventListener("click",function(ev){
    var x=ev.target.closest(".ed-x"); if(x) x.parentNode.remove();
  });
  dlgBody.querySelector("#ed-apply").addEventListener("click",function(){
    var out={};
    var place=dlgBody.querySelector("#ed-place").innerHTML.trim();
    var stack=dlgBody.querySelector("#ed-stack").innerHTML.trim();
    var cite=dlgBody.querySelector("#ed-cite").innerHTML.trim();
    out.place=place; out.stack=stack;
    if(cite) out.cite=cite;
    out.pts=[];
    pts.querySelectorAll(".ed-box").forEach(function(b){
      var v=b.innerHTML.trim(); if(v) out.pts.push(v);
    });
    out.links=[];
    links.querySelectorAll(".ed-item").forEach(function(it){
      var lab=it.querySelector('[data-k="label"]').value.trim();
      var url=it.querySelector('[data-k="url"]').value.trim();
      if(lab&&url) out.links.push([lab,url]);
    });
    out.name=dlgBody.querySelector("#ed-name").innerHTML.trim();
    out.role=dlgBody.querySelector("#ed-role").innerHTML.trim();
    out.when=dlgBody.querySelector("#ed-when").innerHTML.trim();

    /* fold into the live entry and the pending content payload */
    e.name=out.name; e.role=out.role; e.when=out.when;
    setFace(e);
    e.place=out.place; e.stack=out.stack; e.pts=out.pts;
    e.links=out.links.length?out.links:null;
    if(out.cite) e.cite=out.cite; else delete e.cite;
    CONTENT.cards=CONTENT.cards||{};
    var keep=CONTENT.cards[e.id]||{};
    keep.name=out.name; keep.role=out.role; keep.when=out.when;
    keep.place=out.place; keep.stack=out.stack; keep.pts=out.pts; keep.links=out.links;
    if(out.cite) keep.cite=out.cite; else delete keep.cite;
    CONTENT.cards[e.id]=keep;
    refreshCardLinks(e);
    dlg.close ? dlg.close() : dlg.removeAttribute("open");
  });
}
/* card face and modal read from the same entry, so an edit in either place shows in both */
function setFace(e){
  var n=nodeById(e.id); if(!n) return;
  var map={nm:"name",rl:"role",wh:"when"};
  for(var cls in map){
    var el=n.el.querySelector("."+cls);
    if(el && el.innerHTML!==e[map[cls]]) el.innerHTML=e[map[cls]];
  }
  var row=document.querySelector('.list .hit[data-id="'+e.id+'"]');
  if(row){
    var li=row.parentNode;
    ["nm","rl","wh"].forEach(function(cls){
      var el=li.querySelector("."+cls);
      if(el) el.innerHTML=e[map[cls]];
    });
  }
}
function refreshCardLinks(e){
  var n=nodeById(e.id); if(!n) return;
  var old=n.el.querySelector(".ltip"); if(old) old.remove();
  if(e.links&&e.links.length){
    var sp=document.createElement("span"); sp.className="ltip";
    e.links.forEach(function(l){
      var a=document.createElement("a");
      a.href=l[1]; a.target="_blank"; a.rel="noopener"; a.textContent=l[0];
      sp.appendChild(a);
    });
    n.el.appendChild(sp);
  }
}
function nodeById(id){ for(var i=0;i<nodes.length;i++) if(nodes[i].e.id===id) return nodes[i]; return null; }
function byId(id){ for(var i=0;i<ENTRIES.length;i++) if(ENTRIES[i].id===id) return ENTRIES[i]; return null; }
document.getElementById("closeBtn").addEventListener("click",function(){ dlg.close ? dlg.close() : dlg.removeAttribute("open"); });
dlg.addEventListener("click",function(ev){ if(ev.target===dlg){ dlg.close ? dlg.close() : dlg.removeAttribute("open"); } });
dlg.addEventListener("close",function(){ dlgBody.innerHTML=""; if(lastFocus) lastFocus.focus(); });

/* ---------------- cards ---------------- */
var cardsWrap=document.getElementById("cards");
var nodes=[];
ENTRIES.forEach(function(e){
  var b=document.createElement("div");
  b.setAttribute("role","button"); b.tabIndex=0;
  b.className="card"+(e.now?" now":""); b.dataset.cat=e.cat; b.dataset.id=e.id;
  var links="";
  if(e.links){
    links='<span class="ltip">';
    for(var i=0;i<e.links.length;i++)
      links+='<a href="'+e.links[i][1]+'" target="_blank" rel="noopener">'+e.links[i][0]+'</a>';
    links+='</span>';
  }
  var c=(CONTENT.cards&&CONTENT.cards[e.id])||{};
  ["name","role","when","place","stack","cite"].forEach(function(k){
    if(typeof c[k]==="string") e[k]=c[k];
  });
  if(c.pts) e.pts=c.pts;
  if(c.links) e.links=c.links;
  b.innerHTML='<span class="mark"><img src="'+LOGOS[e.logo]+'" alt="" loading="lazy"></span>'+
    '<span><span class="nm">'+e.name+'</span><span class="rl">'+e.role+'</span></span>'+
    '<span class="meta"><span class="dot"></span><span class="wh">'+e.when+'</span>'+
    (e.now?'<span class="live">now</span>':'')+'</span>'+links+
    '<span class="handle h-w" data-h="w"></span><span class="handle h-r" data-h="r"></span>'+
    '<button class="editbtn" type="button" title="Edit details">&#9998;</button>';
  b.addEventListener("click",function(ev){
    if(editing) return;
    if(ev.target.closest(".ltip")) return;
    openDetail(e.id,b);
  });
  b.addEventListener("keydown",function(ev){
    if(editing) return;
    if(ev.key==="Enter"||ev.key===" "){ ev.preventDefault(); openDetail(e.id,b); }
  });
  b.addEventListener("input",function(ev){
    var t=ev.target, map={nm:"name",rl:"role",wh:"when"};
    for(var cls in map) if(t.classList&&t.classList.contains(cls)) e[map[cls]]=t.innerHTML.trim();
  });
  cardsWrap.appendChild(b);
  nodes.push({el:b,e:e});
});

/* ---------------- polar layout ----------------
   angle = category sector, radius = recency (recent sits closer to the name).
   A short relaxation pass then pushes apart any cards that still overlap. */
var stage=document.getElementById("stage"), wires=document.getElementById("wires");
var SECTORS={};                       /* filled per layout, degrees */
var ROOT=document.documentElement;
function hardSmall(){ return window.innerWidth<=900 || window.innerHeight<=600; }

/* Exact overlap test for rotated rectangles (separating axis theorem).
   A bounding-box test is far too loose for tilted cards and would drop a
   perfectly fine layout into list view. GAP grows each rectangle slightly so
   cards that merely touch count as overlapping. */
var GAP=3;
function corners(x,y,w,h,deg){
  var r=(deg||0)*Math.PI/180, c=Math.cos(r), s=Math.sin(r);
  var hw=w/2+GAP, hh=h/2+GAP, out=[];
  [[-hw,-hh],[hw,-hh],[hw,hh],[-hw,hh]].forEach(function(p){
    out.push([x+p[0]*c-p[1]*s, y+p[0]*s+p[1]*c]);
  });
  return out;
}
function overlaps(A,B){
  var quads=[A,B];
  for(var q=0;q<2;q++){
    var P=quads[q];
    for(var i=0;i<4;i++){
      var ax=P[(i+1)%4][0]-P[i][0], ay=P[(i+1)%4][1]-P[i][1];
      var nx=-ay, ny=ax;                       /* axis normal to this edge */
      var a0=Infinity,a1=-Infinity,b0=Infinity,b1=-Infinity;
      for(var k=0;k<4;k++){
        var pa=A[k][0]*nx+A[k][1]*ny; if(pa<a0)a0=pa; if(pa>a1)a1=pa;
        var pb=B[k][0]*nx+B[k][1]*ny; if(pb<b0)b0=pb; if(pb>b1)b1=pb;
      }
      if(a1<b0||b1<a0) return false;           /* a gap on this axis */
    }
  }
  return true;
}
function crowded(cx,cy,hub){
  var boxes=nodes.map(function(n){ return corners(n.x,n.y,n.w,n.h,n.rot); });
  var hubBox=corners(cx,cy,hub.w,hub.h,0);
  for(var i=0;i<boxes.length;i++){
    if(overlaps(boxes[i],hubBox)) return true;
    for(var j=i+1;j<boxes.length;j++)
      if(overlaps(boxes[i],boxes[j])) return true;
  }
  return false;
}

function layout(){
  if(hardSmall()){ ROOT.classList.add("list-mode"); return; }
  ROOT.classList.remove("list-mode");          /* measure with the graph shown */
  var W=stage.clientWidth, H=stage.clientHeight;
  var cx=W/2, cy=H/2;
  var hubEl=document.querySelector(".hub");
  var hub={w:hubEl.offsetWidth, h:hubEl.offsetHeight};
  var counts={};
  CATS.forEach(function(c){ counts[c[0]]=0; });
  ENTRIES.forEach(function(e){ counts[e.cat]++; });

  /* give each category an arc proportional to how many cards it holds */
  var total=ENTRIES.length, gap=7, start=-118;
  SECTOR_ORDER.forEach(function(cat){
    var span=(360-gap*SECTOR_ORDER.length)*(counts[cat]/total);
    SECTORS[cat]={from:start,to:start+span};
    start+=span+gap;
  });

  var rxMin=hub.w/2+150, rxMax=Math.min(W/2-140, rxMin+230);
  var ryMin=hub.h/2+110, ryMax=Math.min(H/2-70, ryMin+180);

  /* every slot the dial offers, in the order the sectors are laid out */
  var slots=[];
  SECTOR_ORDER.forEach(function(cat){
    var count=counts[cat], s=SECTORS[cat];
    for(var i=0;i<count;i++){
      slots.push({
        deg: s.from+(s.to-s.from)*(count===1?0.5:(i+0.5)/count),
        k:   count===1?0.28:i/(count-1)
      });
    }
  });

  ORDER.forEach(function(id,i){
    var n=nodeById(id), sl=slots[i];
    if(!n||!sl) return;
    var rad=sl.deg*Math.PI/180;
    var rx=rxMin+(rxMax-rxMin)*sl.k, ry=ryMin+(ryMax-ryMin)*sl.k;
    var o=(LAYOUT.cards||{})[id];
    if(o&&o.w) n.el.style.width=o.w+"px";
    n.w=n.el.offsetWidth; n.h=n.el.offsetHeight;
    n.deg=sl.deg;
    /* the automatic placement, kept as a fallback even when the card is pinned */
    n.px=cx+Math.cos(rad)*rx; n.py=cy+Math.sin(rad)*ry;
    n.prot=Math.max(-6,Math.min(6,Math.cos(rad)*6.5));
    if(o&&typeof o.fx==="number"&&typeof o.fy==="number"){
      n.pinned=true;
      n.x=o.fx*W; n.y=o.fy*H;
      n.rot=(typeof o.rot==="number")?o.rot:0;
    }else{
      n.pinned=false;
      n.x=cx+Math.cos(rad)*rx; n.y=cy+Math.sin(rad)*ry;
      n.rot=(o&&typeof o.rot==="number")?o.rot:Math.max(-6,Math.min(6,Math.cos(rad)*6.5));
    }
  });

  /* Relaxation: separate overlapping cards, keep clear of the hub and the edges.
     `freeAll` ignores pinning, which is how a hand-placed layout re-flows on a
     smaller screen instead of dropping straight to the list. */
  function relax(freeAll, pad){
    var loose=function(n){ return freeAll || !n.pinned; };
    for(var pass=0;pass<140;pass++){
      for(var i=0;i<nodes.length;i++){
        for(var j=i+1;j<nodes.length;j++){
          var a=nodes[i],b2=nodes[j];
          var dx=b2.x-a.x, dy=b2.y-a.y;
          var ox=(a.w+b2.w)/2+pad-Math.abs(dx), oy=(a.h+b2.h)/2+pad-Math.abs(dy);
          if(ox>0&&oy>0){
            var fa=loose(a), fb=loose(b2);
            if(!fa&&!fb) continue;
            var wa=fa?(fb?0.5:1):0, wb=fb?(fa?0.5:1):0;
            if(ox<oy){ var s1=(dx<0?-1:1)*ox; a.x-=s1*wa; b2.x+=s1*wb; }
            else     { var s2=(dy<0?-1:1)*oy; a.y-=s2*wa; b2.y+=s2*wb; }
          }
        }
      }
      for(var m=0;m<nodes.length;m++){
        var n2=nodes[m];
        if(!loose(n2)) continue;
        var hx=(hub.w+n2.w)/2+22-Math.abs(n2.x-cx), hy=(hub.h+n2.h)/2+16-Math.abs(n2.y-cy);
        if(hx>0&&hy>0){
          if(hx<hy) n2.x+=(n2.x<cx?-1:1)*hx; else n2.y+=(n2.y<cy?-1:1)*hy;
        }
        n2.x=Math.max(n2.w/2+14,Math.min(W-n2.w/2-14,n2.x));
        n2.y=Math.max(n2.h/2+10,Math.min(H-n2.h/2-10,n2.y));
      }
    }
  }

  /* Three chances to keep the graph before falling back to the list:
     1. the pinned arrangement exactly as saved
     2. the same arrangement, but every card free to be nudged
     3. the automatic polar placement, ignoring the saved positions */
  var saved=nodes.map(function(n){ return {x:n.x,y:n.y,rot:n.rot}; });
  relax(false,16);
  var sol=fits(cx,cy,hub,W,H);
  if(!sol){
    nodes.forEach(function(n,i){ n.x=saved[i].x; n.y=saved[i].y; });
    relax(true,14);
    sol=fits(cx,cy,hub,W,H);
  }
  if(!sol){
    nodes.forEach(function(n){ n.x=n.px; n.y=n.py; n.rot=n.prot; });
    relax(true,12);
    sol=fits(cx,cy,hub,W,H);
  }
  if(!sol){ ROOT.classList.add("list-mode"); return; }

  /* Where a ray leaves a box of half-size (hw,hh) that is rotated by `deg`.
     The direction is taken into the box's own frame first, otherwise a tilted
     card's wire stops short of (or on top of) its real border. */
  function edge(dx,dy,hw,hh,inset,deg){
    var lx=dx, ly=dy;
    if(deg){
      var r=-deg*Math.PI/180, c=Math.cos(r), s2=Math.sin(r);
      lx=dx*c-dy*s2; ly=dx*s2+dy*c;
    }
    var ax=Math.abs(lx), ay=Math.abs(ly);
    var t=Math.min(ax>0.001?hw/ax:1e9, ay>0.001?hh/ay:1e9);
    var len=Math.sqrt(dx*dx+dy*dy)||1;
    return t+(inset/len);
  }
  var svg="";
  nodes.forEach(function(n){
    n.el.style.left=Math.round(n.x-n.w/2)+"px";
    n.el.style.top=Math.round(n.y-n.h/2)+"px";
    n.el.style.transform="rotate("+n.rot.toFixed(2)+"deg)";

    var dx=n.x-cx, dy=n.y-cy;
    var t1=edge(dx,dy,hub.w/2,hub.h/2,8,0);       /* leave the hub's border */
    var t2=edge(dx,dy,n.w/2,n.h/2,9,n.rot);       /* stop clear of the card's */
    var x1=cx+dx*t1, y1=cy+dy*t1;
    var x2=n.x-dx*t2, y2=n.y-dy*t2;
    /* if the card is so close the two edges cross, skip the wire */
    if((x2-x1)*dx+(y2-y1)*dy > 0){
      svg+='<line data-cat="'+n.e.cat+'" x1="'+x1.toFixed(1)+'" y1="'+y1.toFixed(1)+
           '" x2="'+x2.toFixed(1)+'" y2="'+y2.toFixed(1)+'"></line>';
    }
  });
  wires.innerHTML=svg;
  paintWires();
  applyArcs(sol);
}

/* Section labels are part of the layout, not an afterthought. Each one is
   searched outward along its sector and slid along the arc until it clears
   every card, the hub and its neighbours; if none of them can be placed, the
   layout counts as not fitting. */
var arcsEl=document.getElementById("arcs");
var arcEls={};
function ensureArcs(){
  SECTOR_ORDER.forEach(function(cat){
    if(arcEls[cat]) return;
    var el=document.createElement("span");
    el.className="arc"; el.dataset.cat=cat;
    el.innerHTML='<span class="arc-t"></span><span class="arc-h"></span>';
    el.firstChild.textContent=catLabel(cat);
    arcsEl.appendChild(el);
    arcEls[cat]=el;
  });
}
function solveArcs(cx,cy,W,H,boxes,hubBox){
  ensureArcs();
  var out=[], placed=[], allOk=true;
  SECTOR_ORDER.forEach(function(cat){
    var sec=SECTORS[cat], el=arcEls[cat];
    if(!sec) return;
    var lw=el.offsetWidth, lh=el.offsetHeight;
    var mid=(sec.from+sec.to)/2;
    var rot=mid+90;
    while(rot>180) rot-=360; while(rot<-180) rot+=360;
    if(rot>90||rot<-90) rot+=180;                    /* never upside down */

    var o=(LAYOUT.arcs||{})[cat]||{};
    if(typeof o.rot==="number") rot=o.rot;
    if(typeof o.fx==="number" && typeof o.fy==="number"){   /* hand-placed */
      var pin={cat:cat,el:el,x:o.fx*W,y:o.fy*H,rot:rot};
      placed.push(corners(pin.x,pin.y,lw,lh,rot));
      out.push(pin);
      return;
    }

    /* how far the cards reach in this direction */
    var ux=Math.cos(mid*Math.PI/180), uy=Math.sin(mid*Math.PI/180), reach=0;
    nodes.forEach(function(n){
      var d=(n.x-cx)*ux+(n.y-cy)*uy;
      if(d>reach) reach=d+Math.abs(n.w/2*ux)+Math.abs(n.h/2*uy);
    });

    function clear(x,y){
      if(x-lw/2<8 || x+lw/2>W-8 || y-lh/2<6 || y+lh/2>H-6) return false;
      var box=corners(x,y,lw,lh,rot);
      if(overlaps(box,hubBox)) return false;
      for(var i=0;i<boxes.length;i++) if(overlaps(box,boxes[i])) return false;
      for(var k=0;k<placed.length;k++) if(overlaps(box,placed[k])) return false;
      return true;
    }

    var found=null, base=reach+30;
    for(var dr=0; dr<=240 && !found; dr+=8){
      for(var da=0; da<=18 && !found; da+=3){
        var signs = da===0 ? [1] : [1,-1];
        for(var q=0;q<signs.length && !found;q++){
          var a=(mid+signs[q]*da)*Math.PI/180;
          var x=cx+Math.cos(a)*(base+dr), y=cy+Math.sin(a)*(base+dr);
          if(clear(x,y)) found={x:x,y:y};
        }
      }
    }
    if(!found){
      allOk=false;
      found={x:cx+ux*base, y:cy+uy*base};
    }
    placed.push(corners(found.x,found.y,lw,lh,rot));
    out.push({cat:cat,el:el,x:found.x,y:found.y,rot:rot});
  });
  out.ok=allOk;
  return out;
}
function applyArcs(sol){
  sol.forEach(function(a){
    var bw=a.el.offsetWidth, bh=a.el.offsetHeight;
    a.el.style.left=Math.round(a.x-bw/2)+"px";
    a.el.style.top=Math.round(a.y-bh/2)+"px";
    a.el.style.transform="rotate("+a.rot.toFixed(1)+"deg)";
  });
  paintArcs();
}
function cardBoxes(){
  return nodes.map(function(n){ return corners(n.x,n.y,n.w,n.h,n.rot); });
}
/* the whole picture fits only if the cards clear each other AND every label
   can be placed; returns the label solution, or null */
function fits(cx,cy,hub,W,H){
  if(crowded(cx,cy,hub)) return null;
  var sol=solveArcs(cx,cy,W,H,cardBoxes(),corners(cx,cy,hub.w,hub.h,0));
  return sol.ok ? sol : null;
}
function redrawArcs(){
  var W=stage.clientWidth,H=stage.clientHeight,cx=W/2,cy=H/2;
  var hubEl=document.querySelector(".hub");
  applyArcs(solveArcs(cx,cy,W,H,cardBoxes(),
    corners(cx,cy,hubEl.offsetWidth,hubEl.offsetHeight,0)));
}
function paintArcs(){
  var as=arcsEl.querySelectorAll(".arc");
  for(var i=0;i<as.length;i++)
    as[i].classList.toggle("on", !active || as[i].dataset.cat===active);
}

/* ---------------- legend / filter ---------------- */
var active=null;
var legend=document.getElementById("legend");
CATS.forEach(function(c){
  var b=document.createElement("button");
  b.type="button"; b.dataset.cat=c[0]; b.setAttribute("aria-pressed","false");
  b.innerHTML='<span class="sw" style="background:var(--c-'+c[0]+')"></span>'+c[1]+
    '<kbd>'+KEYS[c[0]].toUpperCase()+'</kbd>';
  b.addEventListener("click",function(){ setFilter(active===c[0]?null:c[0]); });
  legend.appendChild(b);
});
var clearBtn=document.createElement("button");
clearBtn.type="button"; clearBtn.className="clear"; clearBtn.textContent="Show all";
clearBtn.addEventListener("click",function(){ setFilter(null); });
legend.appendChild(clearBtn);

function paintWires(){
  /* wires stay neutral; the cards alone carry the selection */
  var ls=wires.querySelectorAll("line");
  for(var i=0;i<ls.length;i++){ ls[i].style.opacity=active?"0.35":"0.75"; }
}
function setFilter(cat){
  active=cat;
  stage.classList.toggle("filtered",!!cat);
  nodes.forEach(function(n){ n.el.classList.toggle("on",!cat||n.e.cat===cat); });
  var bs=legend.querySelectorAll("button[data-cat]");
  for(var i=0;i<bs.length;i++)
    bs[i].setAttribute("aria-pressed", bs[i].dataset.cat===cat ? "true":"false");
  clearBtn.hidden=!cat;
  paintWires(); paintArcs();
  document.querySelectorAll(".list [data-group]").forEach(function(g){
    g.hidden = !!cat && g.dataset.group!==cat;
  });
}
clearBtn.hidden=true;

/* ---------------- mobile list ---------------- */
var list=document.getElementById("list");
CATS.forEach(function(c){
  var items=ENTRIES.filter(function(e){ return e.cat===c[0]; });
  if(!items.length) return;
  var sec=document.createElement("section");
  sec.dataset.group=c[0];
  var h='<h2>'+c[1]+'</h2><ul>';
  items.forEach(function(e){
    var links="";
    if(e.links){
      links='<span class="rlinks">';
      for(var i=0;i<e.links.length;i++)
        links+='<a href="'+e.links[i][1]+'" target="_blank" rel="noopener">'+e.links[i][0]+'</a>';
      links+='</span>';
    }
    h+='<li class="rw"><button class="hit" type="button" data-id="'+e.id+'" aria-label="Details for '+e.name+'"></button>'+
       '<span class="mark"><img src="'+LOGOS[e.logo]+'" alt="" loading="lazy"></span>'+
       '<span><span class="nm">'+e.name+'</span><span class="rl">'+e.role+'</span>'+links+'</span>'+
       '<span class="wh">'+e.when+'</span></li>';
  });
  sec.innerHTML=h+'</ul>';
  list.appendChild(sec);
});
list.addEventListener("click",function(ev){
  var b=ev.target.closest(".hit");
  if(b) openDetail(b.dataset.id,b);
});

/* ---------------- saved hub copy ---------------- */
var hubH1=document.querySelector(".hub h1"),
    hubRole=document.querySelector(".hub .role-line"),
    hubBio=document.querySelector(".hub p.bio");
if(CONTENT.hub){
  if(CONTENT.hub.name) hubH1.innerHTML=CONTENT.hub.name;
  if(CONTENT.hub.role) hubRole.innerHTML=CONTENT.hub.role;
  if(CONTENT.hub.bio)  hubBio.innerHTML=CONTENT.hub.bio;
}

/* ---------------- pointers from the copy to a card ---------------- */
document.querySelectorAll(".tip[data-card]").forEach(function(a){
  a.addEventListener("click",function(ev){
    ev.preventDefault();
    var id=a.dataset.card;
    var card=document.querySelector('.card[data-id="'+id+'"]');
    if(card && card.offsetParent!==null){
      card.focus();
      if(card.animate && !reduce) card.animate(
        [{transform:card.style.transform+" scale(1)"},
         {transform:card.style.transform+" scale(1.06)"},
         {transform:card.style.transform+" scale(1)"}],{duration:620,easing:"ease-out"});
    } else {
      var row=document.querySelector('.list .hit[data-id="'+id+'"]');
      if(row) row.scrollIntoView({behavior:reduce?"auto":"smooth",block:"center"});
    }
  });
});

/* ---------------- resume ---------------- */
var rDlg=document.getElementById("resumeDlg");
var dlBtn=document.getElementById("dlBtn"), openBtn=document.getElementById("openBtn"),
    note=document.getElementById("dlNote");
var PDF_B64=dlBtn.getAttribute("href").split(",")[1];
function pdfBytes(){
  var bin=atob(PDF_B64), out=new Uint8Array(bin.length);
  for(var i=0;i<bin.length;i++) out[i]=bin.charCodeAt(i);
  return out;
}
document.getElementById("resumeBtn").addEventListener("click",function(){
  if(rDlg.showModal) rDlg.showModal(); else rDlg.setAttribute("open","");
  sharpen();
});
document.getElementById("resumeClose").addEventListener("click",function(){
  rDlg.close ? rDlg.close() : rDlg.removeAttribute("open");
});
rDlg.addEventListener("click",function(ev){ if(ev.target===rDlg){ rDlg.close ? rDlg.close() : rDlg.removeAttribute("open"); } });

var drawnAt=0;
function sharpen(){
  var lib=window.pdfjsLib, cv=document.getElementById("pdfCanvas"), im=document.getElementById("pdfImg");
  if(!lib||!cv) return;
  var cssW=cv.parentNode.clientWidth;
  if(!cssW || (drawnAt && Math.abs(cssW-drawnAt)<24)) return;
  var dpr=Math.min(window.devicePixelRatio||1,3);
  try{ lib.GlobalWorkerOptions.workerSrc="https://cdnjs.cloudflare.com/ajax/libs/pdf.js/3.11.174/pdf.worker.min.js"; }catch(e){}
  lib.getDocument({data:pdfBytes()}).promise.then(function(doc){ return doc.getPage(1); })
  .then(function(page){
    var base=page.getViewport({scale:1});
    var vp=page.getViewport({scale:(cssW*dpr)/base.width});
    cv.width=Math.round(vp.width); cv.height=Math.round(vp.height);
    return page.render({canvasContext:cv.getContext("2d"),viewport:vp}).promise;
  }).then(function(){ drawnAt=cssW; cv.hidden=false; if(im) im.hidden=true; })
  .catch(function(){});
}
fetch("Kanav_Bengani_Resume.pdf",{method:"HEAD"}).then(function(r){
  if(r.ok) dlBtn.href="Kanav_Bengani_Resume.pdf";
}).catch(function(){ openBtn.href=dlBtn.href; });

var saver=null;
if(window.claude&&typeof window.claude.use==="function"){
  window.claude.use("downloads").then(function(d){ saver=d; }).catch(function(){});
}
dlBtn.addEventListener("click",function(ev){
  if(!saver||dlBtn.getAttribute("href").indexOf("data:")!==0) return;
  ev.preventDefault();
  note.textContent="Saving...";
  saver.save({filename:"Kanav_Bengani_Resume.pdf",data:pdfBytes()})
    .then(function(){ note.textContent="Saved."; })
    .catch(function(err){
      var c=err&&err.code;
      note.textContent = c==="declined" ? "" :
        c==="rate_limited" ? "Try that again in a moment." :
        "Download unavailable here. Use Open in new tab.";
    });
});

/* ---------------- click the background to clear the selection ---------------- */
document.addEventListener("click",function(ev){
  if(!active) return;
  if(ev.target.closest(".legend,.card,.ltip,dialog,a,button")) return;
  setFilter(null);
});

/* ---------------- keyboard: w a s d pick a category, twice clears ---------------- */
var KEYCAT={};
for(var kc in KEYS) KEYCAT[KEYS[kc]]=kc;
document.addEventListener("keydown",function(ev){
  if(ev.metaKey||ev.ctrlKey||ev.altKey) return;
  if(dlg.open||rDlg.open) return;
  var t=ev.target;
  if(t&&(t.tagName==="INPUT"||t.tagName==="TEXTAREA"||t.isContentEditable)) return;
  var k=(ev.key||"").toLowerCase();
  if(k==="escape"){ if(active) setFilter(null); return; }
  var cat=KEYCAT[k];
  if(!cat) return;
  ev.preventDefault();
  setFilter(active===cat ? null : cat);
});


/* ================= local editor hook =================
   Nothing below ships to a real host: on any non-localhost origin the
   browser never requests editor.js, so the edit UI does not exist there. */
if(LOCAL){
  window.__kb={
    nodes:nodes, nodeById:nodeById, LAYOUT:LAYOUT, CONTENT:CONTENT,
    layout:layout, stage:stage, wires:wires, arcsEl:arcsEl,
    paintWires:paintWires, redrawArcs:redrawArcs, dlg:dlg, openDetail:openDetail,
    hub:{h1:hubH1, role:hubRole, bio:hubBio},
    setEditing:function(v){ editing=!!v; }
  };
  var _s=document.createElement("script");
  _s.src="editor.js"; _s.defer=true;
  document.head.appendChild(_s);
}

/* ---------------- go ---------------- */
layout();

/* Locally the JSON files are the source of truth, so pick up anything saved
   since the last build without needing to re-run build.py. */
if(LOCAL){
  Promise.all([
    fetch("layout.json",{cache:"no-store"}).then(function(r){return r.ok?r.json():null;}).catch(function(){return null;}),
    fetch("content.json",{cache:"no-store"}).then(function(r){return r.ok?r.json():null;}).catch(function(){return null;})
  ]).then(function(res){
    var lay=res[0], con=res[1], touched=false;
    if(lay&&lay.cards){ LAYOUT.cards=lay.cards; LAYOUT.arcs=lay.arcs||{}; touched=true; }
    if(con){
      if(con.hub){
        if(con.hub.name) hubH1.innerHTML=con.hub.name;
        if(con.hub.role) hubRole.innerHTML=con.hub.role;
        if(con.hub.bio)  hubBio.innerHTML=con.hub.bio;
      }
      if(con.cards) nodes.forEach(function(n){
        var c=con.cards[n.e.id]; if(!c) return;
        [["nm","name"],["rl","role"],["wh","when"]].forEach(function(p){
          var el=n.el.querySelector("."+p[0]);
          if(el&&c[p[1]]) el.innerHTML=c[p[1]];
        });
      });
      touched=true;
    }
    if(touched) layout();
  });
}
window.addEventListener("load",function(){ layout(); if(rDlg.open) sharpen(); });
var rt=null;
window.addEventListener("resize",function(){
  clearTimeout(rt);
  rt=setTimeout(function(){ layout(); if(rDlg.open) sharpen(); },130);
});
})();
</script>
"""

used = sorted({e["logo"] for e in DATA})
html = (HTML
  .replace("__LOGOS__", json.dumps({k: L[k] for k in used}, separators=(",", ":")))
  .replace("__ENTRIES__", js_entries())
  .replace("__CATS__", json.dumps(CATS))
  .replace("__SECTORS__", json.dumps(SECTOR_ORDER))
  .replace("__KEYS__", json.dumps(KEYS))
  .replace("__ORDER__", json.dumps(ORDER))
  .replace("__LAYOUT__", json.dumps(LAYOUT))
  .replace("__CONTENT__", json.dumps(CONTENT, ensure_ascii=True))
  .replace("__PREVIEW__", PREVIEW)
  .replace("__PDF__", PDF))

EDITOR_JS = open(os.path.join(HERE, "_editor_src.js"), encoding="utf-8").read()
with open(os.path.join(HERE, "editor.js"), "w", encoding="utf-8") as fh:
    fh.write(EDITOR_JS)
print("wrote", os.path.join(HERE, "editor.js"), len(EDITOR_JS), "bytes")

out = os.path.join(HERE, "index.html")
open(out, "wb").write(html.encode("ascii", "xmlcharrefreplace"))
print("wrote", out, os.path.getsize(out), "bytes")
