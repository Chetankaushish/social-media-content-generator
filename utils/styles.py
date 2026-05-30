"""
UI Styling — Dark Futuristic Theme
All custom CSS injected into Streamlit.
"""

DARK_FUTURISTIC_CSS = """
<style>

/* ── Google Fonts ── */
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&family=Orbitron:wght@400;700;900&display=swap');

/* ── CSS Variables ── */
:root {
    --bg-primary: #050810;
    --bg-secondary: #0a0f1e;
    --bg-card: #0d1428;
    --bg-glass: rgba(13, 20, 40, 0.7);
    --border-glow: rgba(0, 212, 255, 0.25);
    --border-subtle: rgba(255, 255, 255, 0.06);
    --accent-cyan: #00d4ff;
    --accent-purple: #7b61ff;
    --accent-green: #00ff9d;
    --accent-orange: #ff6b35;
    --text-primary: #e8edf7;
    --text-secondary: #8896b3;
    --text-muted: #4a5568;
    --font-display: 'Orbitron', monospace;
    --font-body: 'Space Grotesk', sans-serif;
    --font-mono: 'JetBrains Mono', monospace;
    --glow-cyan: 0 0 20px rgba(0, 212, 255, 0.3);
    --glow-purple: 0 0 20px rgba(123, 97, 255, 0.3);
}

/* ── Global Reset ── */
.stApp {
    background: var(--bg-primary) !important;
    font-family: var(--font-body) !important;
    color: var(--text-primary) !important;
}

/* Animated grid background */
.stApp::before {
    content: '';
    position: fixed;
    top: 0; left: 0; right: 0; bottom: 0;
    background-image: 
        linear-gradient(rgba(0, 212, 255, 0.03) 1px, transparent 1px),
        linear-gradient(90deg, rgba(0, 212, 255, 0.03) 1px, transparent 1px);
    background-size: 60px 60px;
    pointer-events: none;
    z-index: 0;
}

/* ── Header ── */
.main-header {
    text-align: center;
    padding: 2.5rem 0 1.5rem;
    position: relative;
}

.main-header h1 {
    font-family: var(--font-display) !important;
    font-size: 2.4rem !important;
    font-weight: 900 !important;
    letter-spacing: 0.12em !important;
    background: linear-gradient(135deg, #00d4ff 0%, #7b61ff 50%, #00ff9d 100%) !important;
    -webkit-background-clip: text !important;
    -webkit-text-fill-color: transparent !important;
    background-clip: text !important;
    margin: 0 !important;
    text-transform: uppercase !important;
}

.main-header .subtitle {
    font-family: var(--font-mono);
    font-size: 0.78rem;
    color: var(--text-muted);
    letter-spacing: 0.25em;
    text-transform: uppercase;
    margin-top: 0.5rem;
}

.header-line {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent-cyan), var(--accent-purple), transparent);
    margin: 1.5rem 0;
    opacity: 0.6;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}

section[data-testid="stSidebar"] .stMarkdown p {
    color: var(--text-secondary) !important;
    font-family: var(--font-body) !important;
}

.sidebar-section-label {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    color: var(--accent-cyan);
    text-transform: uppercase;
    margin-bottom: 0.5rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid var(--border-subtle);
}

/* ── Cards ── */
.content-card {
    background: var(--bg-glass);
    border: 1px solid var(--border-subtle);
    border-radius: 12px;
    padding: 1.5rem;
    margin-bottom: 1rem;
    position: relative;
    backdrop-filter: blur(10px);
    transition: border-color 0.3s ease, box-shadow 0.3s ease;
}

.content-card:hover {
    border-color: var(--border-glow);
    box-shadow: var(--glow-cyan);
}

.content-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0;
    width: 3px; height: 100%;
    border-radius: 12px 0 0 12px;
    background: linear-gradient(180deg, var(--accent-cyan), var(--accent-purple));
}

.variation-number {
    font-family: var(--font-mono);
    font-size: 0.65rem;
    color: var(--accent-cyan);
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-bottom: 0.75rem;
}

.variation-text {
    font-family: var(--font-body);
    font-size: 0.95rem;
    line-height: 1.7;
    color: var(--text-primary);
    white-space: pre-wrap;
    word-break: break-word;
}

/* ── Platform Badges ── */
.platform-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    padding: 0.25rem 0.75rem;
    border-radius: 20px;
    font-family: var(--font-mono);
    font-size: 0.7rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 1rem;
}

.badge-twitter { background: rgba(0, 212, 255, 0.1); border: 1px solid rgba(0, 212, 255, 0.4); color: #00d4ff; }
.badge-linkedin { background: rgba(0, 160, 220, 0.1); border: 1px solid rgba(0, 160, 220, 0.4); color: #00a0dc; }
.badge-instagram { background: rgba(247, 119, 55, 0.1); border: 1px solid rgba(247, 119, 55, 0.4); color: #f77737; }
.badge-facebook { background: rgba(24, 119, 242, 0.1); border: 1px solid rgba(24, 119, 242, 0.4); color: #1877f2; }

/* ── Char Counter ── */
.char-counter {
    font-family: var(--font-mono);
    font-size: 0.7rem;
    margin-top: 0.5rem;
    text-align: right;
}
.char-safe { color: var(--accent-green); }
.char-warning { color: #f5a623; }
.char-over { color: #ff4757; }

/* ── Hashtag Block ── */
.hashtag-block {
    background: rgba(123, 97, 255, 0.08);
    border: 1px solid rgba(123, 97, 255, 0.25);
    border-radius: 8px;
    padding: 1rem;
    font-family: var(--font-mono);
    font-size: 0.82rem;
    color: #a78bff;
    line-height: 1.8;
    margin-top: 0.5rem;
}

/* ── Hook Block ── */
.hook-item {
    background: rgba(0, 212, 255, 0.05);
    border-left: 2px solid var(--accent-cyan);
    padding: 0.75rem 1rem;
    margin-bottom: 0.6rem;
    border-radius: 0 8px 8px 0;
    font-size: 0.9rem;
    color: var(--text-primary);
    font-style: italic;
}

/* ── Streamlit Inputs ── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.9rem !important;
    transition: border-color 0.2s ease !important;
}

.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-cyan) !important;
    box-shadow: 0 0 0 1px rgba(0, 212, 255, 0.2) !important;
}

.stSelectbox > div > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-primary) !important;
}

/* ── Buttons ── */
.stButton > button {
    background: linear-gradient(135deg, #00d4ff, #7b61ff) !important;
    color: #050810 !important;
    border: none !important;
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.55rem 1.4rem !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 0 15px rgba(0, 212, 255, 0.2) !important;
}

.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px rgba(0, 212, 255, 0.4) !important;
}

.stButton > button:active {
    transform: translateY(0) !important;
}

/* Secondary buttons (copy etc.) */
.stButton > button[kind="secondary"] {
    background: transparent !important;
    border: 1px solid var(--border-subtle) !important;
    color: var(--text-secondary) !important;
    box-shadow: none !important;
}

.stButton > button[kind="secondary"]:hover {
    border-color: var(--accent-cyan) !important;
    color: var(--accent-cyan) !important;
    box-shadow: none !important;
    transform: none !important;
}

/* ── Tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: var(--bg-secondary) !important;
    border-bottom: 1px solid var(--border-subtle) !important;
    gap: 0 !important;
}

.stTabs [data-baseweb="tab"] {
    background: transparent !important;
    color: var(--text-muted) !important;
    font-family: var(--font-body) !important;
    font-size: 0.85rem !important;
    letter-spacing: 0.05em !important;
    padding: 0.75rem 1.25rem !important;
    border: none !important;
    border-bottom: 2px solid transparent !important;
    transition: all 0.2s ease !important;
}

.stTabs [aria-selected="true"] {
    color: var(--accent-cyan) !important;
    border-bottom: 2px solid var(--accent-cyan) !important;
    background: transparent !important;
}

/* ── Slider ── */
.stSlider > div > div > div > div {
    background: linear-gradient(90deg, var(--accent-cyan), var(--accent-purple)) !important;
}

/* ── Radio ── */
.stRadio > div {
    gap: 0.5rem !important;
}

.stRadio [data-testid="stMarkdownContainer"] p {
    color: var(--text-secondary) !important;
    font-family: var(--font-body) !important;
}

/* ── Success/Error alerts ── */
.stAlert {
    border-radius: 8px !important;
    font-family: var(--font-body) !important;
}

/* ── Spinner ── */
.stSpinner > div {
    border-top-color: var(--accent-cyan) !important;
}

/* ── Dividers ── */
hr {
    border-color: var(--border-subtle) !important;
}

/* ── Scrollbar ── */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg-primary); }
::-webkit-scrollbar-thumb { background: var(--border-glow); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--accent-cyan); }

/* ── Labels ── */
.stTextInput label, .stTextArea label, .stSelectbox label, 
.stSlider label, .stRadio label, .stMultiSelect label {
    color: var(--text-secondary) !important;
    font-family: var(--font-body) !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
}

/* ── Expander ── */
.streamlit-expanderHeader {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
    color: var(--text-secondary) !important;
    font-family: var(--font-body) !important;
}

/* ── Info boxes ── */
.stat-pill {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(0, 212, 255, 0.07);
    border: 1px solid rgba(0, 212, 255, 0.15);
    border-radius: 6px;
    padding: 0.3rem 0.7rem;
    font-family: var(--font-mono);
    font-size: 0.72rem;
    color: var(--text-secondary);
}

.stat-pill span { color: var(--accent-cyan); font-weight: 600; }

/* ── Status indicator ── */
.status-dot {
    display: inline-block;
    width: 7px; height: 7px;
    border-radius: 50%;
    background: var(--accent-green);
    box-shadow: 0 0 8px var(--accent-green);
    animation: pulse-dot 2s infinite;
}

@keyframes pulse-dot {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* ── Section headers ── */
.section-header {
    font-family: var(--font-mono);
    font-size: 0.68rem;
    letter-spacing: 0.2em;
    color: var(--accent-cyan);
    text-transform: uppercase;
    margin-bottom: 1rem;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

.section-header::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border-subtle);
}

/* ── Multiselect ── */
.stMultiSelect > div {
    background: var(--bg-card) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 8px !important;
}

</style>
"""


def render_header():
    return """
    <div class="main-header">
        <h1>⚡ ContentForge AI</h1>
        <p class="subtitle">// Powered by Gemini · LangChain · Built for creators</p>
    </div>
    <div class="header-line"></div>
    """


def render_platform_badge(platform: str) -> str:
    slug = platform.lower().replace("/", "").replace(" ", "")
    icons = {
        "twitterx": "𝕏",
        "linkedin": "in",
        "instagram": "◎",
        "facebook": "f",
    }
    icon = icons.get(slug, "◈")
    return f'<div class="platform-badge badge-{slug}">{icon} &nbsp; {platform}</div>'


def render_content_card(variation_num: int, content: str, char_info: tuple) -> str:
    used, limit, status = char_info
    status_class = f"char-{status}"
    return f"""
    <div class="content-card">
        <div class="variation-number">▸ Variation {variation_num}</div>
        <div class="variation-text">{content}</div>
        <div class="char-counter {status_class}">{used:,} / {limit:,} chars</div>
    </div>
    """


def render_hashtag_block(hashtags: str) -> str:
    return f'<div class="hashtag-block">{hashtags}</div>'


def render_hook_item(hook: str) -> str:
    return f'<div class="hook-item">{hook}</div>'


def render_stat_pill(label: str, value: str) -> str:
    return f'<span class="stat-pill">{label}: <span>{value}</span></span>'


def render_section_header(title: str) -> str:
    return f'<div class="section-header">◈ {title}</div>'
