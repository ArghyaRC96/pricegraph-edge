import streamlit as st
from textwrap import dedent

def _html(content):
    content = dedent(content).strip()
    if hasattr(st, "html"):
        st.html(content)
    else:
        st.markdown(content, unsafe_allow_html=True)

def inject_theme():
    _html("""
    <style>
    :root{
      --ink:#162033;--muted:#667085;--purple:#6C5CE7;--cyan:#12B5CB;
      --coral:#FF7A7A;--green:#12A67B;--surface:rgba(255,255,255,.82);
      --border:rgba(56,48,110,.10);
    }
    .stApp{
      background:
        radial-gradient(circle at 8% 4%,rgba(75,180,255,.22),transparent 28%),
        radial-gradient(circle at 91% 3%,rgba(169,137,255,.23),transparent 28%),
        radial-gradient(circle at 72% 96%,rgba(255,154,190,.20),transparent 32%),
        linear-gradient(135deg,#f9fcff 0%,#f7f5ff 48%,#fff9fc 100%);
      color:var(--ink);
    }
    [data-testid="stHeader"]{background:rgba(255,255,255,.55);backdrop-filter:blur(16px)}
    .block-container{max-width:1450px;padding-top:2rem;padding-bottom:4rem}
    section[data-testid="stSidebar"]{
      background:linear-gradient(180deg,rgba(255,255,255,.96),rgba(247,249,255,.94));
      border-right:1px solid rgba(80,70,130,.10);box-shadow:14px 0 40px rgba(48,44,92,.05)
    }
    section[data-testid="stSidebar"] *{color:#26324A!important}
    section[data-testid="stSidebar"] a{border-radius:12px;transition:.18s ease}
    section[data-testid="stSidebar"] a:hover{background:rgba(108,92,231,.08)}
    section[data-testid="stSidebar"] a[aria-current="page"]{
      background:linear-gradient(90deg,rgba(108,92,231,.13),rgba(18,181,203,.10));
      border:1px solid rgba(108,92,231,.15);font-weight:700
    }
    h1,h2,h3,h4{color:#162033!important;letter-spacing:-.03em}
    p,label,li,[data-testid="stMarkdownContainer"]{color:#4d5870}
    .pg-hero{
      position:relative;overflow:hidden;padding:3.3rem 3.3rem;border-radius:34px;
      background:linear-gradient(125deg,rgba(255,255,255,.95),rgba(250,249,255,.82));
      border:1px solid rgba(108,92,231,.12);
      box-shadow:0 26px 75px rgba(83,72,132,.12);margin-bottom:1.5rem
    }
    .pg-hero-grid{display:grid;grid-template-columns:1.25fr .75fr;gap:2rem;align-items:center}
    .pg-eyebrow{color:#6C5CE7;font-size:.77rem;font-weight:850;letter-spacing:.18em;text-transform:uppercase;margin-bottom:1rem}
    .pg-title{font-size:clamp(3.5rem,6vw,6.2rem);line-height:.91;letter-spacing:-.075em;font-weight:950;
      background:linear-gradient(105deg,#16233A 3%,#6551D8 42%,#0B94B1 72%,#D34A91 100%);
      -webkit-background-clip:text;-webkit-text-fill-color:transparent}
    .pg-subtitle{max-width:760px;margin-top:1.4rem;color:#5E687D;font-size:1.03rem;line-height:1.7}
    .pg-badges{display:flex;flex-wrap:wrap;gap:.55rem;margin-top:1.2rem}
    .pg-badge{padding:.45rem .75rem;border-radius:999px;background:rgba(255,255,255,.85);
      border:1px solid rgba(108,92,231,.13);box-shadow:0 8px 22px rgba(79,70,125,.06);
      color:#4b566e;font-size:.75rem;font-weight:750}
    .pg-orbit{width:100%;max-width:370px;margin:auto;filter:drop-shadow(0 18px 35px rgba(90,80,150,.13))}
    .pg-card{min-height:146px;padding:1.35rem 1.4rem;border-radius:23px;
      background:linear-gradient(145deg,rgba(255,255,255,.91),rgba(248,250,255,.77));
      border:1px solid var(--border);box-shadow:0 16px 46px rgba(74,67,112,.08);transition:.2s ease}
    .pg-card:hover{transform:translateY(-3px);box-shadow:0 22px 52px rgba(74,67,112,.12);border-color:rgba(108,92,231,.24)}
    .pg-card-label{color:#7a8499;font-size:.7rem;font-weight:850;text-transform:uppercase;letter-spacing:.11em}
    .pg-card-value{margin-top:.66rem;color:#162033;font-size:2.35rem;font-weight:900;letter-spacing:-.05em;line-height:1}
    .pg-card-caption{margin-top:.66rem;color:#7a8498;font-size:.82rem;line-height:1.45}
    .pg-section{margin-top:2.4rem;margin-bottom:1.1rem}
    .pg-section-kicker{color:#6C5CE7;font-size:.7rem;font-weight:850;letter-spacing:.16em;text-transform:uppercase}
    .pg-section-title{margin-top:.25rem;color:#162033;font-size:2.05rem;font-weight:900;letter-spacing:-.045em}
    .pg-section-copy{max-width:820px;margin-top:.4rem;color:#6b7487;line-height:1.65}
    .pg-pagehead{padding:1.5rem 0 .6rem}
    .pg-pagehead h1{font-size:3rem!important;margin:.15rem 0 .5rem!important}
    .pg-pagehead p{font-size:1rem;max-width:820px}
    div[data-testid="stMetric"]{background:rgba(255,255,255,.78);border:1px solid var(--border);
      padding:1rem;border-radius:20px;box-shadow:0 12px 34px rgba(70,64,105,.06)}
    div[data-testid="stDataFrame"]{border-radius:18px;overflow:hidden;border:1px solid var(--border)}
    div[data-baseweb="select"]>div,div[data-testid="stNumberInput"] input,div[data-testid="stTextInput"] input,textarea{
      background:rgba(255,255,255,.92)!important;color:#162033!important;border-color:rgba(80,70,130,.15)!important;border-radius:13px!important}
    .stButton>button{border:0;border-radius:14px;padding:.7rem 1.15rem;background:linear-gradient(100deg,#6C5CE7,#5B79DE,#13A3BE);
      color:white;font-weight:800;box-shadow:0 12px 28px rgba(95,77,210,.20)}
    .stButton>button:hover{color:white;transform:translateY(-1px)}
    div[data-testid="stAlert"]{border-radius:16px}
    @media(max-width:900px){.pg-hero-grid{grid-template-columns:1fr}.pg-orbit{max-width:280px}.pg-hero{padding:2rem}}
    footer{visibility:hidden}
    </style>
    """)

def hero():
    _html("""
    <div class="pg-hero">
      <div class="pg-hero-grid">
        <div>
          <div class="pg-eyebrow">Retail pricing intelligence</div>
          <div class="pg-title">PRICEGRAPH<br>EDGE</div>
          <div class="pg-subtitle">Predict demand, simulate supported prices, and expose cross-product pricing relationships in one decision system.</div>
          <div class="pg-badges">
            <span class="pg-badge">Poisson XGBoost</span><span class="pg-badge">Safe Price Simulation</span>
            <span class="pg-badge">Cross-Price Graph</span><span class="pg-badge">Gemini Analyst</span>
          </div>
        </div>
        <div>
          <svg class="pg-orbit" viewBox="0 0 380 300" xmlns="http://www.w3.org/2000/svg">
            <defs>
              <linearGradient id="g1" x1="0" x2="1"><stop stop-color="#6C5CE7"/><stop offset="1" stop-color="#12B5CB"/></linearGradient>
              <filter id="shadow"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-opacity=".13"/></filter>
            </defs>
            <rect x="18" y="18" width="344" height="264" rx="34" fill="#ffffff" fill-opacity=".56" stroke="#6C5CE7" stroke-opacity=".10"/>
            <path d="M78 205 C125 118 177 105 245 82" fill="none" stroke="#6C5CE7" stroke-width="5" stroke-linecap="round" opacity=".55"/>
            <path d="M78 205 C150 205 208 222 304 173" fill="none" stroke="#12B5CB" stroke-width="5" stroke-linecap="round" opacity=".50"/>
            <path d="M245 82 C275 110 282 135 304 173" fill="none" stroke="#D34A91" stroke-width="4" stroke-linecap="round" opacity=".45"/>
            <circle cx="78" cy="205" r="24" fill="url(#g1)" filter="url(#shadow)"/>
            <circle cx="245" cy="82" r="21" fill="#6C5CE7" filter="url(#shadow)"/>
            <circle cx="304" cy="173" r="22" fill="#12B5CB" filter="url(#shadow)"/>
            <circle cx="173" cy="150" r="29" fill="#ffffff" stroke="#6C5CE7" stroke-width="5" filter="url(#shadow)"/>
            <text x="173" y="155" text-anchor="middle" font-size="12" font-family="Arial" font-weight="700" fill="#3E3A61">PRICE</text>
            <text x="78" y="246" text-anchor="middle" font-size="12" font-family="Arial" font-weight="700" fill="#58627A">DEMAND</text>
            <text x="245" y="49" text-anchor="middle" font-size="12" font-family="Arial" font-weight="700" fill="#58627A">GRAPH</text>
            <text x="304" y="211" text-anchor="middle" font-size="12" font-family="Arial" font-weight="700" fill="#58627A">REVENUE</text>
          </svg>
        </div>
      </div>
    </div>
    """)

def page_header(kicker, title, copy):
    _html(f"""
    <div class="pg-pagehead">
      <div class="pg-eyebrow">{kicker}</div>
      <h1>{title}</h1>
      <p>{copy}</p>
    </div>
    """)

def metric_card(label, value, caption=""):
    _html(f"""
    <div class="pg-card">
      <div class="pg-card-label">{label}</div>
      <div class="pg-card-value">{value}</div>
      <div class="pg-card-caption">{caption}</div>
    </div>
    """)

def section_header(kicker, title, copy=""):
    _html(f"""
    <div class="pg-section">
      <div class="pg-section-kicker">{kicker}</div>
      <div class="pg-section-title">{title}</div>
      <div class="pg-section-copy">{copy}</div>
    </div>
    """)

def artifact_missing(names):
    st.info("This page is ready. Sync these generated artifacts to activate the live data: " + ", ".join(names))
