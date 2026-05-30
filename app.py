"""
ContentForge AI — Social Media Content Generator
Built with Streamlit + LangChain + Anthropic Claude

Run: streamlit run app.py
"""

import streamlit as st
import os
from dotenv import load_dotenv

from utils.generator import (
    SocialContentGenerator,
    PLATFORM_CONFIGS,
    TONES,
    CONTENT_TYPES,
    get_char_status,
    validate_api_key,
)
from utils.styles import (
    DARK_FUTURISTIC_CSS,
    render_header,
    render_platform_badge,
    render_content_card,
    render_hashtag_block,
    render_hook_item,
    render_stat_pill,
    render_section_header,
)
from utils.session import (
    init_session_state,
    save_to_history,
    get_history,
    clear_history,
    toggle_saved,
)

# ── Page config (must be first Streamlit call) ─────────────────────────────────
st.set_page_config(
    page_title="ContentForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

load_dotenv()
init_session_state()

# ── Inject CSS ─────────────────────────────────────────────────────────────────
st.markdown(DARK_FUTURISTIC_CSS, unsafe_allow_html=True)
st.markdown(render_header(), unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(
        '<p class="sidebar-section-label">⚙ Configuration</p>',
        unsafe_allow_html=True,
    )


    if api_key_input and api_key_input != st.session_state.api_key:
        with st.spinner("Validating key..."):
            if validate_api_key(api_key_input):
                st.session_state.api_key = api_key_input
                st.session_state.api_key_validated = True
                st.session_state.generator = SocialContentGenerator(api_key=api_key_input)
                st.success("✓ Connected to Gemini")
            else:
                st.error("✗ Invalid API key")
                st.session_state.api_key_validated = False

    if st.session_state.api_key_validated:
        st.markdown(
            '<span class="status-dot"></span>&nbsp; <span style="font-size:0.75rem;color:#8896b3;">Gemini API active</span>',
            unsafe_allow_html=True,
        )

    st.divider()

    # ── Platform selector ────────────────────────────────────────────────────
    st.markdown(
        '<p class="sidebar-section-label">◈ Target Platform</p>',
        unsafe_allow_html=True,
    )
    selected_platform = st.selectbox(
        "Platform",
        options=list(PLATFORM_CONFIGS.keys()),
        label_visibility="collapsed",
    )

    platform_config = PLATFORM_CONFIGS[selected_platform]
    st.markdown(
        render_stat_pill("Char limit", f"{platform_config['char_limit']:,}"),
        unsafe_allow_html=True,
    )

    st.divider()

    # ── Content settings ─────────────────────────────────────────────────────
    st.markdown(
        '<p class="sidebar-section-label">◈ Content Settings</p>',
        unsafe_allow_html=True,
    )

    selected_content_type = st.selectbox("Content Type", CONTENT_TYPES)
    selected_tone = st.selectbox("Tone", TONES)
    num_variations = st.slider("Variations to generate", min_value=1, max_value=5, value=3)

    st.divider()

    # ── History summary ──────────────────────────────────────────────────────
    history = get_history()
    if history:
        st.markdown(
            '<p class="sidebar-section-label">◈ Session History</p>',
            unsafe_allow_html=True,
        )
        st.markdown(
            render_stat_pill("Generated", str(len(history))),
            unsafe_allow_html=True,
        )
        saved_count = sum(1 for r in history if r.get("saved"))
        if saved_count:
            st.markdown(
                f'&nbsp;{render_stat_pill("Saved", str(saved_count))}',
                unsafe_allow_html=True,
            )
        if st.button("Clear History", key="clear_hist"):
            clear_history()
            st.rerun()


# ═══════════════════════════════════════════════════════════════════════════════
# MAIN CONTENT — TABS
# ═══════════════════════════════════════════════════════════════════════════════

tab_generate, tab_hooks, tab_repurpose, tab_history = st.tabs([
    "⚡ Generate", "🪝 Hook Generator", "🔄 Repurpose", "📁 History"
])


# ── Tab 1: Generate ────────────────────────────────────────────────────────────
with tab_generate:
    col_left, col_right = st.columns([1, 1.1], gap="large")

    with col_left:
        st.markdown(render_section_header("Brief"), unsafe_allow_html=True)

        topic = st.text_area(
            "Topic / Brief",
            placeholder="e.g. Launching our new AI writing tool that saves 3 hours/day for marketers...",
            height=110,
            label_visibility="collapsed",
        )

        audience = st.text_input(
            "Target Audience",
            placeholder="e.g. SaaS founders, marketing managers aged 28–45",
        )

        col_kw, col_inst = st.columns(2)
        with col_kw:
            keywords = st.text_input(
                "Keywords (optional)",
                placeholder="e.g. AI, productivity, ROI",
            )
        with col_inst:
            extra_instructions = st.text_input(
                "Special Instructions",
                placeholder="e.g. Mention our 14-day free trial",
            )

        # Generate button
        st.markdown("<br>", unsafe_allow_html=True)
        gen_col, _ = st.columns([1, 2])
        with gen_col:
            generate_clicked = st.button(
                f"⚡ Generate {num_variations} Variations",
                use_container_width=True,
                disabled=not st.session_state.api_key_validated,
            )

        if not st.session_state.api_key_validated:
            st.caption("⚠ Add your API key in the sidebar to start generating.")

    with col_right:
        st.markdown(render_section_header("Output"), unsafe_allow_html=True)

        if generate_clicked:
            if not topic.strip():
                st.error("Please enter a topic or brief.")
            elif not audience.strip():
                st.error("Please describe your target audience.")
            else:
                with st.spinner(f"Crafting {num_variations} variations for {selected_platform}..."):
                    try:
                        results = st.session_state.generator.generate_content(
                            platform=selected_platform,
                            topic=topic,
                            content_type=selected_content_type,
                            desired_tone=selected_tone,
                            audience=audience,
                            num_variations=num_variations,
                            extra_instructions=extra_instructions,
                            keywords=keywords,
                        )
                        st.session_state.current_results = results
                        st.session_state.current_hashtags = {}
                        save_to_history(
                            platform=selected_platform,
                            topic=topic,
                            content_type=selected_content_type,
                            variations=results["variations"],
                        )
                    except Exception as e:
                        st.error(f"Generation failed: {str(e)}")

        if st.session_state.current_results:
            results = st.session_state.current_results
            st.markdown(
                render_platform_badge(results["platform"]),
                unsafe_allow_html=True,
            )

            for i, variation in enumerate(results["variations"], 1):
                char_info = get_char_status(variation, results["platform"])
                st.markdown(
                    render_content_card(i, variation, char_info),
                    unsafe_allow_html=True,
                )

                btn_col1, btn_col2 = st.columns(2)
                with btn_col1:
                    if st.button(f"Copy #{i}", key=f"copy_{i}"):
                        st.code(variation, language=None)

                with btn_col2:
                    if st.button(f"Get Hashtags #{i}", key=f"hashtag_{i}"):
                        with st.spinner("Finding best hashtags..."):
                            try:
                                ht = st.session_state.generator.generate_hashtags(
                                    platform=results["platform"],
                                    content=variation,
                                    topic=topic,
                                )
                                st.session_state.current_hashtags[i] = ht
                            except Exception as e:
                                st.error(f"Error: {str(e)}")

                if i in st.session_state.current_hashtags:
                    st.markdown(
                        render_hashtag_block(st.session_state.current_hashtags[i]),
                        unsafe_allow_html=True,
                    )

                st.markdown("<br>", unsafe_allow_html=True)


# ── Tab 2: Hook Generator ──────────────────────────────────────────────────────
with tab_hooks:
    st.markdown(render_section_header("Hook Generator"), unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#8896b3;font-size:0.88rem;margin-bottom:1.5rem;">Generate 5 scroll-stopping opening lines using different psychological techniques.</p>',
        unsafe_allow_html=True,
    )

    h_col1, h_col2 = st.columns([1, 1.1], gap="large")

    with h_col1:
        hook_topic = st.text_area(
            "What's the hook for?",
            placeholder="e.g. Why most people fail at building habits — and the 5-minute fix",
            height=100,
        )
        hook_tone = st.selectbox("Tone", TONES, key="hook_tone")
        hook_platform = st.selectbox("Platform", list(PLATFORM_CONFIGS.keys()), key="hook_platform")

        hook_btn = st.button(
            "🪝 Generate Hooks",
            disabled=not st.session_state.api_key_validated,
        )

    with h_col2:
        if hook_btn:
            if not hook_topic.strip():
                st.error("Enter a topic for your hooks.")
            else:
                with st.spinner("Crafting hooks that stop thumbs..."):
                    try:
                        hooks = st.session_state.generator.generate_hooks(
                            platform=hook_platform,
                            topic=hook_topic,
                            tone=hook_tone,
                        )
                        st.session_state.current_hooks = hooks
                    except Exception as e:
                        st.error(f"Error: {str(e)}")

        if st.session_state.current_hooks:
            techniques = [
                "Bold Statement", "Stat / Surprise", "Pain Point ?",
                "Story Opener", "Counter-Intuitive",
            ]
            for i, hook in enumerate(st.session_state.current_hooks):
                label = techniques[i] if i < len(techniques) else f"Hook {i+1}"
                st.markdown(
                    f'<div style="font-family:\'JetBrains Mono\',monospace;font-size:0.62rem;color:#00d4ff;letter-spacing:0.15em;text-transform:uppercase;margin-bottom:0.3rem;">{label}</div>',
                    unsafe_allow_html=True,
                )
                st.markdown(render_hook_item(hook), unsafe_allow_html=True)


# ── Tab 3: Repurpose ───────────────────────────────────────────────────────────
with tab_repurpose:
    st.markdown(render_section_header("Repurpose Content"), unsafe_allow_html=True)
    st.markdown(
        '<p style="color:#8896b3;font-size:0.88rem;margin-bottom:1.5rem;">Adapt existing content to feel native on a different platform.</p>',
        unsafe_allow_html=True,
    )

    r_col1, r_col2 = st.columns([1, 1], gap="large")

    with r_col1:
        original_content = st.text_area(
            "Original Content",
            placeholder="Paste your existing post here...",
            height=180,
        )
        rc1, rc2 = st.columns(2)
        with rc1:
            source_platform = st.selectbox("From Platform", list(PLATFORM_CONFIGS.keys()), key="src_platform")
        with rc2:
            target_platform = st.selectbox("To Platform", list(PLATFORM_CONFIGS.keys()), index=1, key="tgt_platform")

        repurpose_btn = st.button(
            "🔄 Repurpose Content",
            disabled=not st.session_state.api_key_validated,
        )

    with r_col2:
        if repurpose_btn:
            if not original_content.strip():
                st.error("Paste some content to repurpose.")
            elif source_platform == target_platform:
                st.error("Source and target platforms must be different.")
            else:
                with st.spinner(f"Adapting for {target_platform}..."):
                    try:
                        repurposed = st.session_state.generator.repurpose_content(
                            original_content=original_content,
                            source_platform=source_platform,
                            target_platform=target_platform,
                        )
                        char_info = get_char_status(repurposed, target_platform)
                        st.markdown(
                            render_platform_badge(target_platform),
                            unsafe_allow_html=True,
                        )
                        st.markdown(
                            render_content_card(1, repurposed, char_info),
                            unsafe_allow_html=True,
                        )
                    except Exception as e:
                        st.error(f"Error: {str(e)}")


# ── Tab 4: History ─────────────────────────────────────────────────────────────
with tab_history:
    st.markdown(render_section_header("Generation History"), unsafe_allow_html=True)

    history = get_history()

    if not history:
        st.markdown(
            '<p style="color:#4a5568;font-size:0.9rem;text-align:center;padding:3rem 0;">No generations yet. Go to ⚡ Generate to create your first content.</p>',
            unsafe_allow_html=True,
        )
    else:
        for record in history:
            saved_icon = "⭐" if record.get("saved") else "☆"
            with st.expander(
                f"{saved_icon}  [{record['platform']}]  {record['topic']}  ·  {record['timestamp']}"
            ):
                st.markdown(
                    f'<div style="display:flex;gap:0.5rem;flex-wrap:wrap;margin-bottom:1rem;">'
                    f'{render_stat_pill("Platform", record["platform"])}'
                    f'&nbsp;{render_stat_pill("Type", record["content_type"])}'
                    f'&nbsp;{render_stat_pill("Variations", str(len(record["variations"])))}'
                    f"</div>",
                    unsafe_allow_html=True,
                )

                for i, variation in enumerate(record["variations"], 1):
                    char_info = get_char_status(variation, record["platform"])
                    st.markdown(
                        render_content_card(i, variation, char_info),
                        unsafe_allow_html=True,
                    )

                save_col, _ = st.columns([1, 3])
                with save_col:
                    label = "★ Unsave" if record.get("saved") else "☆ Save"
                    if st.button(label, key=f"save_{record['id']}"):
                        toggle_saved(record["id"])
                        st.rerun()


# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown(
    """
    <div style="text-align:center;padding:1.5rem 0;border-top:1px solid rgba(255,255,255,0.05);">
        <span style="font-family:'JetBrains Mono',monospace;font-size:0.65rem;color:#2d3748;letter-spacing:0.2em;">
            CONTENTFORGE AI &nbsp;·&nbsp; LANGCHAIN + GOOGLE GEMINI &nbsp;·&nbsp; BUILT FOR CREATORS
        </span>
    </div>
    """,
    unsafe_allow_html=True,
)
