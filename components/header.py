import streamlit as st
from pathlib import Path

def load_css():
    """Loads the custom pastel CSS styles."""
    css_path = Path(__file__).parent.parent / "assets" / "style.css"
    if css_path.exists():
        with open(css_path, "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

def render_hero(title: str, subtitle: str, icon: str = "🍽️"):
    """Renders a modern pastel hero banner."""
    load_css()
    html = f"""
    <div class="hero-container">
        <div class="hero-title">{icon} {title}</div>
        <div class="hero-subtitle">{subtitle}</div>
    </div>
    """
    st.markdown(html, unsafe_allow_html=True)
