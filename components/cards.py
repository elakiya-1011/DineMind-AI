import streamlit as st

def render_feature_card(icon: str, title: str, description: str, badges: list = None):
    """Renders a modern pastel card with high contrast text."""
    badge_html = ""
    if badges:
        for b_text, b_type in badges:
            badge_html += f"<span class='badge-pill badge-{b_type}'>{b_text}</span>"
            
    card_html = f"""
    <div class="dinemind-card">
        <div class="card-icon">{icon}</div>
        <div class="card-title">{title}</div>
        <div class="card-desc">{description}</div>
        <div style="margin-top: 1rem;">{badge_html}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)

def render_metric_card(label: str, value: str, subtext: str = ""):
    """Renders a compact metric box with high contrast typography."""
    card_html = f"""
    <div class="metric-box">
        <div class="metric-label">{label}</div>
        <div class="metric-val">{value}</div>
        <div class="metric-sub">{subtext}</div>
    </div>
    """
    st.markdown(card_html, unsafe_allow_html=True)
