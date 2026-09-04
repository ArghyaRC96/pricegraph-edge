import html
import streamlit as st


def _render(content):
    st.html(content)


def inject_theme():

    _render("""
    <style>

    :root {
        --bg1: #d9dee8;
        --bg2: #e4dfe9;
        --bg3: #d7e4e5;

        --surface: rgba(246, 247, 250, 0.88);
        --surface2: rgba(237, 240, 246, 0.88);

        --text: #182238;
        --soft: #58667c;
        --muted: #788398;

        --purple: #6657d8;
        --teal: #11888f;
        --pink: #c94f86;

        --border: rgba(74, 67, 120, 0.15);
        --shadow: 0 16px 42px rgba(42, 48, 72, 0.10);
    }


    .stApp {
        background:
            radial-gradient(
                circle at 8% 8%,
                rgba(17, 136, 143, 0.11),
                transparent 28%
            ),
            radial-gradient(
                circle at 90% 12%,
                rgba(102, 87, 216, 0.13),
                transparent 30%
            ),
            radial-gradient(
                circle at 72% 90%,
                rgba(201, 79, 134, 0.09),
                transparent 25%
            ),
            linear-gradient(
                135deg,
                var(--bg1),
                var(--bg2) 50%,
                var(--bg3)
            );

        color: var(--text);
    }


    [data-testid="stHeader"] {
        background: rgba(220, 225, 235, 0.64);
        backdrop-filter: blur(15px);
    }


    .block-container {
        max-width: 1450px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    section[data-testid="stSidebar"] {
        background:
            linear-gradient(
                180deg,
                rgba(230, 234, 242, 0.98),
                rgba(216, 224, 235, 0.98)
            );

        border-right: 1px solid var(--border);
    }


    section[data-testid="stSidebar"] * {
        color: var(--text) !important;
    }


    section[data-testid="stSidebar"] a {
        border-radius: 13px;
    }


    section[data-testid="stSidebar"] a:hover {
        background:
            linear-gradient(
                90deg,
                rgba(102, 87, 216, 0.10),
                rgba(17, 136, 143, 0.08)
            );
    }


    section[data-testid="stSidebar"] a[aria-current="page"] {
        background:
            linear-gradient(
                90deg,
                rgba(102, 87, 216, 0.16),
                rgba(17, 136, 143, 0.11)
            );

        border: 1px solid rgba(102, 87, 216, 0.18);
        font-weight: 800;
    }


    h1, h2, h3, h4 {
        color: var(--text) !important;
    }


    .pg-hero {
        position: relative;
        overflow: hidden;

        padding: 3rem;
        margin-bottom: 1.6rem;

        border-radius: 30px;

        background:
            linear-gradient(
                135deg,
                rgba(246, 247, 251, 0.91),
                rgba(232, 235, 244, 0.87)
            );

        border: 1px solid var(--border);

        box-shadow: var(--shadow);
    }


    .pg-hero::before {
        content: "";

        position: absolute;

        width: 300px;
        height: 300px;

        right: -100px;
        top: -150px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(102, 87, 216, 0.22),
                transparent 68%
            );
    }


    .pg-hero::after {
        content: "";

        position: absolute;

        width: 260px;
        height: 260px;

        left: 30%;
        bottom: -190px;

        border-radius: 50%;

        background:
            radial-gradient(
                circle,
                rgba(17, 136, 143, 0.20),
                transparent 68%
            );
    }


    .pg-eyebrow,
    .pg-page-kicker,
    .pg-section-kicker {
        position: relative;
        z-index: 2;

        color: var(--purple);

        font-size: 0.72rem;
        font-weight: 850;

        letter-spacing: 0.18em;
        text-transform: uppercase;
    }


    .pg-title {
        position: relative;
        z-index: 2;

        margin-top: 0.7rem;

        font-size: clamp(3.4rem, 6vw, 6rem);
        font-weight: 950;

        line-height: 0.92;
        letter-spacing: -0.065em;

        background:
            linear-gradient(
                100deg,
                #182238,
                #6254d4 45%,
                #11888f 75%,
                #c94f86
            );

        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }


    .pg-subtitle,
    .pg-page-copy,
    .pg-section-copy {
        position: relative;
        z-index: 2;

        color: var(--soft);

        line-height: 1.7;
    }


    .pg-subtitle {
        max-width: 800px;
        margin-top: 1.3rem;
        font-size: 1.04rem;
    }


    .pg-badges {
        position: relative;
        z-index: 2;

        display: flex;
        flex-wrap: wrap;

        gap: 0.55rem;
        margin-top: 1.2rem;
    }


    .pg-badge {
        padding: 0.46rem 0.78rem;

        border-radius: 999px;

        background:
            linear-gradient(
                90deg,
                rgba(102, 87, 216, 0.09),
                rgba(17, 136, 143, 0.07)
            );

        border: 1px solid rgba(102, 87, 216, 0.13);

        color: var(--text);

        font-size: 0.76rem;
        font-weight: 750;
    }


    .pg-card {
        min-height: 150px;

        padding: 1.3rem 1.35rem;

        border-radius: 22px;

        background:
            linear-gradient(
                145deg,
                var(--surface),
                var(--surface2)
            );

        border: 1px solid var(--border);

        box-shadow:
            0 12px 32px rgba(42, 48, 72, 0.08);

        transition: 0.18s ease;
    }


    .pg-card:hover {
        transform: translateY(-3px);
        border-color: rgba(102, 87, 216, 0.26);
        box-shadow: var(--shadow);
    }


    .pg-card-label {
        color: #707c92;

        font-size: 0.72rem;
        font-weight: 850;

        letter-spacing: 0.13em;
        text-transform: uppercase;
    }


    .pg-card-value {
        color: var(--text);

        margin-top: 0.7rem;

        font-size: 2.4rem;
        font-weight: 950;

        line-height: 1;
        letter-spacing: -0.055em;
    }


    .pg-card-caption {
        color: var(--muted);

        margin-top: 0.7rem;

        font-size: 0.84rem;
    }


    .pg-page-header {
        padding: 0.5rem 0 1rem;
    }


    .pg-page-title {
        color: var(--text);

        margin-top: 0.25rem;

        font-size: 3rem;
        font-weight: 950;

        letter-spacing: -0.055em;
    }


    .pg-page-copy {
        max-width: 850px;
        margin-top: 0.45rem;
    }


    .pg-section-kicker {
        margin-top: 2.2rem;
    }


    .pg-section-title {
        color: var(--text);

        margin-top: 0.25rem;

        font-size: 2rem;
        font-weight: 900;

        letter-spacing: -0.045em;
    }


    .pg-section-copy {
        max-width: 840px;

        margin-top: 0.35rem;
        margin-bottom: 1.2rem;
    }


    div[data-baseweb="select"] > div,
    div[data-testid="stNumberInput"] input,
    div[data-testid="stTextInput"] input,
    textarea {
        background: rgba(244, 246, 250, 0.92) !important;

        color: var(--text) !important;

        border-color: rgba(102, 87, 216, 0.15) !important;

        border-radius: 13px !important;
    }


    div[data-testid="stDataFrame"] {
        border-radius: 18px;
        overflow: hidden;

        border: 1px solid var(--border);
    }


    div[data-testid="stMetric"] {
        background: var(--surface);

        border: 1px solid var(--border);
        border-radius: 20px;

        padding: 1rem;
    }


    .stButton > button {
        border: none !important;
        border-radius: 14px !important;

        background:
            linear-gradient(
                100deg,
                var(--purple),
                var(--teal)
            );

        color: white !important;

        font-weight: 800 !important;

        box-shadow:
            0 11px 28px rgba(102, 87, 216, 0.18);
    }


    footer {
        visibility: hidden;
    }

    </style>
    """)


def inject_global_css():
    inject_theme()


def inject_global_styles():
    inject_theme()


def hero():

    _render("""
    <div class="pg-hero">

        <div class="pg-eyebrow">
            Retail Pricing Intelligence
        </div>

        <div class="pg-title">
            PRICEGRAPH<br>EDGE
        </div>

        <div class="pg-subtitle">
            Demand forecasting, supported price simulation,
            cross-product pricing intelligence and AI-assisted
            decision support in one connected retail system.
        </div>

        <div class="pg-badges">
            <span class="pg-badge">Poisson XGBoost</span>
            <span class="pg-badge">Price Simulation</span>
            <span class="pg-badge">PriceGraph</span>
            <span class="pg-badge">Gemini Analyst</span>
        </div>

    </div>
    """)


def render_hero():
    hero()


def page_header(kicker, title, copy=""):

    kicker = html.escape(str(kicker))
    title = html.escape(str(title))
    copy = html.escape(str(copy))

    _render(
        f"""
        <div class="pg-page-header">

            <div class="pg-page-kicker">
                {kicker}
            </div>

            <div class="pg-page-title">
                {title}
            </div>

            <div class="pg-page-copy">
                {copy}
            </div>

        </div>
        """
    )


def metric_card(label, value, caption=""):

    label = html.escape(str(label))
    value = html.escape(str(value))
    caption = html.escape(str(caption))

    _render(
        f"""
        <div class="pg-card">

            <div class="pg-card-label">
                {label}
            </div>

            <div class="pg-card-value">
                {value}
            </div>

            <div class="pg-card-caption">
                {caption}
            </div>

        </div>
        """
    )


def section_header(kicker, title, copy=""):

    kicker = html.escape(str(kicker))
    title = html.escape(str(title))
    copy = html.escape(str(copy))

    _render(
        f"""
        <div class="pg-section-kicker">
            {kicker}
        </div>

        <div class="pg-section-title">
            {title}
        </div>

        <div class="pg-section-copy">
            {copy}
        </div>
        """
    )


def artifact_missing(name):

    st.warning(
        "Required production artifact is missing: "
        + str(name)
    )