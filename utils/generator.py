"""
Content Generation Engine
Handles all LangChain + Google Gemini interactions for social media content creation.
"""

from langchain_google_genai import ChatGoogleGenerativeAI
import google.generativeai as genai
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser


# ── Platform configs ──────────────────────────────────────────────────────────

PLATFORM_CONFIGS = {
    "Twitter/X": {
        "char_limit": 280,
        "icon": "𝕏",
        "color": "#1a1a1a",
        "accent": "#00d4ff",
        "tone_hint": "punchy, witty, conversational. Use hooks, threads feel, hashtags (2–3 max).",
        "format_hint": "Keep it under 280 characters. One powerful sentence or a short thread opener.",
    },
    "LinkedIn": {
        "char_limit": 3000,
        "icon": "in",
        "color": "#0077b5",
        "accent": "#00a0dc",
        "tone_hint": "professional yet human, insightful, story-driven. Show expertise without jargon.",
        "format_hint": "Start with a bold hook. Use line breaks generously. End with a CTA or question. 3–5 paragraphs.",
    },
    "Instagram": {
        "char_limit": 2200,
        "icon": "📸",
        "color": "#e1306c",
        "accent": "#f77737",
        "tone_hint": "inspiring, aesthetic, aspirational. Visual storytelling in words. Emoji-forward.",
        "format_hint": "Engaging opener. Short punchy paragraphs. 5–10 relevant hashtags at the end.",
    },
    "Facebook": {
        "char_limit": 63206,
        "icon": "f",
        "color": "#1877f2",
        "accent": "#42a5f5",
        "tone_hint": "warm, community-focused, conversational. Encourage discussion and sharing.",
        "format_hint": "Friendly opening. Storytelling body. End with a question to spark comments.",
    },
}

TONES = ["Professional", "Casual", "Humorous", "Inspirational", "Urgent", "Educational"]
CONTENT_TYPES = ["Post / Caption", "Thread Opener", "Announcement", "Story / Reel Script", "Poll Question", "Promotional Ad"]


# ── Prompt Templates ──────────────────────────────────────────────────────────

GENERATION_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        """You are an elite social media copywriter with 10+ years of experience crafting 
viral content for Fortune 500 brands and indie creators alike. You understand platform 
algorithms, audience psychology, and what makes content stop thumbs mid-scroll.

Your writing is always:
- Authentic and human — never sounds AI-generated
- Platform-native — you know the culture of each app
- Strategically crafted — every word earns its place
- Engaging — drives likes, shares, saves, and comments

Never use filler phrases like "In today's digital landscape" or "I'm excited to share".
Write like a sharp human, not a corporate bot.""",
    ),
    (
        "human",
        """Create {num_variations} distinct variation(s) of social media content.

PLATFORM: {platform}
PLATFORM TONE: {tone_hint}
FORMAT GUIDANCE: {format_hint}
CHARACTER LIMIT: {char_limit} characters

CONTENT TYPE: {content_type}
DESIRED TONE: {desired_tone}
TOPIC / BRIEF: {topic}
TARGET AUDIENCE: {audience}
{extra_context}

Requirements:
- Each variation must feel genuinely different (not just synonyms swapped)
- Stay within the character limit for the platform
- Make it feel written by a real, talented human
- Optimize for engagement on {platform}

Format your response EXACTLY like this — no extra commentary:

---VARIATION 1---
[content here]

---VARIATION 2---
[content here]

(and so on for each variation)""",
    ),
])

HASHTAG_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You are a social media strategist who knows which hashtags actually drive reach vs. the ones that get ignored. Be concise and strategic.",
    ),
    (
        "human",
        """Generate the optimal hashtags for this content on {platform}.

Content: {content}
Topic: {topic}

Rules:
- Mix of high-volume (broad reach) + niche (targeted reach) hashtags
- Make them relevant and specific
- Twitter/X: 2–3 hashtags max
- Instagram: 8–15 hashtags
- LinkedIn: 3–5 hashtags  
- Facebook: 2–4 hashtags

Return ONLY the hashtags, space-separated, starting with #. No explanation.""",
    ),
])

HOOK_PROMPT = ChatPromptTemplate.from_messages([
    (
        "system",
        "You write scroll-stopping opening lines. Every hook you write makes people stop, read, and engage.",
    ),
    (
        "human",
        """Write 5 powerful hook variations for this topic on {platform}.

Topic: {topic}
Tone: {tone}

Each hook should use a different technique:
1. Bold statement / controversial take
2. Surprising statistic or fact (can be hypothetical, clearly labeled)
3. Question that hits a pain point
4. Story opener ("I once...", "Last week...", "3 years ago...")
5. Counter-intuitive truth

Format: Return ONLY the 5 hooks, numbered 1–5. No labels, no explanation.""",
    ),
])


# ── Generator Class ───────────────────────────────────────────────────────────

class SocialContentGenerator:
    """Main content generation engine powered by LangChain + Google Gemini."""

    def __init__(self, api_key: str, model: str = "gemini-1.5-pro"):
        self.llm = ChatGoogleGenerativeAI(
            model=model,
            google_api_key=api_key,
            temperature=0.85,
            max_output_tokens=4096,
        )
        self.parser = StrOutputParser()

        # Build chains
        self.content_chain = GENERATION_PROMPT | self.llm | self.parser
        self.hashtag_chain = HASHTAG_PROMPT | self.llm | self.parser
        self.hook_chain = HOOK_PROMPT | self.llm | self.parser

    def generate_content(
        self,
        platform: str,
        topic: str,
        content_type: str,
        desired_tone: str,
        audience: str,
        num_variations: int = 3,
        extra_instructions: str = "",
        keywords: str = "",
    ) -> dict:
        """Generate social media content variations with optional hashtags."""

        config = PLATFORM_CONFIGS[platform]
        extra_context = ""
        if extra_instructions:
            extra_context += f"\nSPECIAL INSTRUCTIONS: {extra_instructions}"
        if keywords:
            extra_context += f"\nKEYWORDS TO INCLUDE: {keywords}"

        raw_output = self.content_chain.invoke({
            "platform": platform,
            "tone_hint": config["tone_hint"],
            "format_hint": config["format_hint"],
            "char_limit": config["char_limit"],
            "content_type": content_type,
            "desired_tone": desired_tone,
            "topic": topic,
            "audience": audience,
            "num_variations": num_variations,
            "extra_context": extra_context,
        })

        variations = self._parse_variations(raw_output)
        return {
            "variations": variations,
            "platform": platform,
            "config": config,
        }

    def generate_hashtags(self, platform: str, content: str, topic: str) -> str:
        """Generate optimized hashtags for a piece of content."""
        return self.hashtag_chain.invoke({
            "platform": platform,
            "content": content,
            "topic": topic,
        }).strip()

    def generate_hooks(self, platform: str, topic: str, tone: str) -> list[str]:
        """Generate 5 scroll-stopping hook variations."""
        raw = self.hook_chain.invoke({
            "platform": platform,
            "topic": topic,
            "tone": tone,
        })
        hooks = []
        for line in raw.strip().split("\n"):
            line = line.strip()
            if line and line[0].isdigit() and ". " in line:
                hooks.append(line.split(". ", 1)[1].strip())
            elif line and not line[0].isdigit():
                hooks.append(line)
        return [h for h in hooks if h][:5]

    def repurpose_content(self, original_content: str, source_platform: str, target_platform: str) -> str:
        """Repurpose content from one platform to another."""
        target_config = PLATFORM_CONFIGS[target_platform]
        repurpose_prompt = ChatPromptTemplate.from_messages([
            ("system", "You are an expert at adapting content across social media platforms while preserving the core message and making it feel native to each platform."),
            ("human", f"""Repurpose this {source_platform} content for {target_platform}.

Original content:
{original_content}

Target platform tone: {target_config['tone_hint']}
Format guidance: {target_config['format_hint']}
Character limit: {target_config['char_limit']}

Adapt it fully — don't just copy-paste with minor edits. Make it feel like it was written for {target_platform} from the start.
Return ONLY the repurposed content, no explanation."""),
        ])
        chain = repurpose_prompt | self.llm | self.parser
        return chain.invoke({}).strip()

    def _parse_variations(self, raw_output: str) -> list[str]:
        """Parse the LLM output into individual content variations."""
        variations = []
        parts = raw_output.split("---VARIATION")
        for part in parts[1:]:
            if "---" in part:
                content = part.split("---", 1)[1].strip()
                if content:
                    variations.append(content)
        if not variations:
            variations = [raw_output.strip()]
        return variations


# ── Utility helpers ───────────────────────────────────────────────────────────

def count_chars(text: str) -> int:
    return len(text)


def get_char_status(text: str, platform: str) -> tuple[int, int, str]:
    """Returns (used, limit, status_label)."""
    used = count_chars(text)
    limit = PLATFORM_CONFIGS[platform]["char_limit"]
    if used <= limit * 0.8:
        status = "safe"
    elif used <= limit:
        status = "warning"
    else:
        status = "over"
    return used, limit, status


def validate_api_key(api_key: str) -> bool:
    """Quick validation that the Google Gemini API key works."""
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        model.generate_content("Hi")
        return True
    except Exception:
        return False
