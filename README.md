# ⚡ ContentForge AI
### Social Media Content Generator · LangChain + Anthropic Claude + Streamlit

A dark, futuristic AI-powered content creation tool that generates platform-native social media copy for Twitter/X, LinkedIn, Instagram, and Facebook.

---

## Features

- **Multi-Platform Content Generation** — tailored tone, format, and character limits per platform
- **Multiple Variations** — generate 1–5 distinct variations per run
- **Hook Generator** — 5 scroll-stopping openers using different psychological techniques
- **Hashtag Optimizer** — context-aware hashtags for each platform
- **Content Repurposing** — adapt content from one platform to another
- **Generation History** — session-based history with save/star functionality
- **Dark Futuristic UI** — Orbitron + Space Grotesk fonts, cyan/purple glow aesthetic

---

## Setup

### 1. Clone / download the project

```bash
cd social-content-gen
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv venv
source venv/bin/activate        # macOS/Linux
venv\Scripts\activate           # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set your Anthropic API key

**Option A — `.env` file (recommended):**
```bash
cp .env.example .env
# Edit .env and paste your key:
# ANTHROPIC_API_KEY=sk-ant-...
```

**Option B — Enter it in the sidebar UI** (no `.env` needed)

Get your key at: https://console.anthropic.com

### 5. Run the app

```bash
streamlit run app.py
```

Open http://localhost:8501 in your browser.

---

## Project Structure

```
social-content-gen/
├── app.py                  # Main Streamlit application
├── requirements.txt
├── .env.example
└── utils/
    ├── generator.py        # LangChain + Claude content engine
    ├── styles.py           # Dark futuristic CSS + HTML renderers
    └── session.py          # Session state & history management
```

---

## How It Works

1. **`utils/generator.py`** — The brain. Uses LangChain `ChatPromptTemplate` chains to call Claude claude-3-5-sonnet. Three chains: content generation, hashtag optimization, hook writing.
2. **`utils/styles.py`** — All CSS (CSS variables, grid background, glassmorphism cards, glow effects) + HTML helper functions.
3. **`utils/session.py`** — Streamlit `session_state` wrappers for history tracking.
4. **`app.py`** — Orchestrates sidebar config, 4 tabs (Generate / Hooks / Repurpose / History), and wires everything together.

---

## Customization

| What | Where |
|------|-------|
| Add a new platform | `PLATFORM_CONFIGS` in `utils/generator.py` |
| Change Claude model | `SocialContentGenerator.__init__` → `model=` param |
| Tweak prompts | `GENERATION_PROMPT`, `HASHTAG_PROMPT`, `HOOK_PROMPT` in `generator.py` |
| Change colors/fonts | CSS variables at top of `DARK_FUTURISTIC_CSS` in `styles.py` |
| Adjust temperature | `ChatAnthropic(temperature=...)` in `generator.py` |

---

## Tech Stack

| Layer | Tech |
|-------|------|
| UI | Streamlit 1.35 |
| LLM Orchestration | LangChain 0.2 |
| AI Model | Anthropic Claude 3.5 Sonnet |
| Styling | Custom CSS (glassmorphism, Orbitron font) |
| State | Streamlit session_state |
