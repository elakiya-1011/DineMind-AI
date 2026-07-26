import streamlit as st
from components.header import render_hero, load_css
from components.sidebar import render_sidebar
from components.cards import render_feature_card

st.set_page_config(
    page_title="DineMind AI - Restaurant Customer Assistant",
    page_icon="🍽️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load CSS & Sidebar
load_css()
render_sidebar()

# Hero Section Banner
render_hero(
    title="DineMind AI",
    subtitle="AI-Powered Restaurant Customer Assistant using LangChain, RAG & AI Orchestration",
    icon="🍽️"
)

# Call to Action Navigation Row (3 Core Buttons)
st.markdown("### 🚀 Quick Action Portal")
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("💬 Customer Chat", use_container_width=True, type="primary"):
        st.switch_page("pages/1_Customer_Chat.py")

with col2:
    if st.button("📚 Knowledge Base", use_container_width=True):
        st.switch_page("pages/3_Knowledge_Base.py")

with col3:
    if st.button("🔐 Admin Dashboard", use_container_width=True):
        st.switch_page("pages/2_Admin_Dashboard.py")

st.markdown("---")

# High Contrast Overview Section
st.markdown("## 📌 What is DineMind AI?")
st.markdown("""
**DineMind AI** is an enterprise-grade AI Customer Concierge built specifically for modern restaurants. 
It combines **Retrieval-Augmented Generation (RAG)** with **LangChain Orchestration** to deliver accurate, 
strictly-grounded answers regarding menu offerings, opening hours, allergy indicators, delivery policies, and promotional offers.

> **Zero-Hallucination Guarantee**: DineMind AI answers **ONLY** using verified facts present in official restaurant documents. If requested information is missing from the knowledge base, the system politely informs the customer rather than hallucinating.
""")

# Core Features Grid
st.markdown("## 🌟 Core Application Features")
f_col1, f_col2, f_col3 = st.columns(3)

with f_col1:
    render_feature_card(
        icon="💬",
        title="Customer AI Assistant",
        description="Interactive natural language chat assistant equipped with simulated ordering, menu recommendations, conversation memory, and anti-hallucination guardrails.",
        badges=[("Grounded QA", "coral"), ("Cart Active", "mint")]
    )

with f_col2:
    render_feature_card(
        icon="📚",
        title="Knowledge Base Viewer",
        description="Browse all available restaurant documents (PDF, CSV, TXT, MD). View file attributes, preview text, download files, delete, or replace documents on demand.",
        badges=[("Multi-Format", "blue"), ("Real-Time Sync", "purple")]
    )

with f_col3:
    render_feature_card(
        icon="🔐",
        title="Admin Control Hub",
        description="Secure management portal (admin / admin123). Upload custom documents, monitor indexing health, inspect vector chunk counts, and rebuild ChromaDB.",
        badges=[("Admin Security", "purple"), ("Live Rebuild", "coral")]
    )

st.markdown("---")

# Generative AI Core Concepts
st.markdown("## 🧠 Core Technologies & Concepts")
c_col1, c_col2, c_col3 = st.columns(3)

with c_col1:
    render_feature_card(
        icon="🦜🔗",
        title="What is LangChain?",
        description="LangChain is a framework for developing applications powered by language models. It provides LCEL (LangChain Expression Language) to chain prompts, vector retrievers, custom tools, memory, and output parsers.",
        badges=[("LCEL Runnable", "blue"), ("Chains & Routers", "mint")]
    )

with c_col2:
    render_feature_card(
        icon="📚",
        title="What is RAG?",
        description="Retrieval-Augmented Generation enhances LLM responses by fetching relevant context chunks from a private vector store (ChromaDB) before sending the prompt to OpenAI.",
        badges=[("ChromaDB Vectorstore", "purple"), ("OpenAI Embeddings", "coral")]
    )

with c_col3:
    render_feature_card(
        icon="⚙️",
        title="What is AI Orchestration?",
        description="AI Orchestration controls the complete AI system workflow—managing intent classification, dynamic prompt selection, session cart commands, and self-reflection validation.",
        badges=[("Intent Routing", "mint"), ("Self Reflection", "blue")]
    )

st.markdown("---")
st.markdown("<div style='text-align: center; color: #475569; font-weight: 600; font-size: 0.9rem;'>Built with Streamlit • LangChain • ChromaDB • OpenAI</div>", unsafe_allow_html=True)
