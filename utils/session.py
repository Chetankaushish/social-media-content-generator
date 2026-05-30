"""
Session state management and content history tracking.
"""

import streamlit as st
from datetime import datetime


def init_session_state():
    """Initialize all session state variables."""
    defaults = {
        "api_key_validated": False,
        "api_key": "",
        "generator": None,
        "history": [],          # list of generation records
        "current_results": None,
        "current_hashtags": {},
        "current_hooks": [],
        "generating": False,
        "active_tab": "generate",
    }
    for key, val in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = val


def save_to_history(platform: str, topic: str, content_type: str, variations: list[str]):
    """Save a generation result to session history."""
    record = {
        "id": len(st.session_state.history) + 1,
        "timestamp": datetime.now().strftime("%H:%M · %b %d"),
        "platform": platform,
        "topic": topic[:60] + ("..." if len(topic) > 60 else ""),
        "content_type": content_type,
        "variations": variations,
        "saved": False,
    }
    st.session_state.history.insert(0, record)
    # Keep last 20 records
    st.session_state.history = st.session_state.history[:20]


def get_history():
    return st.session_state.history


def clear_history():
    st.session_state.history = []


def toggle_saved(record_id: int):
    for record in st.session_state.history:
        if record["id"] == record_id:
            record["saved"] = not record["saved"]
            break
