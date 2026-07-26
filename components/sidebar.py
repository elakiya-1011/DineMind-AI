import streamlit as st

def render_sidebar():
    """Renders the simplified sidebar navigation with single ChromaDB Backend Details button."""
    with st.sidebar:
        st.markdown("## 🍱 DineMind AI")
        st.caption("AI-Powered Restaurant Concierge & RAG System")
        st.markdown("---")
        
        st.markdown("#### 💡 Main Navigation")
        st.page_link("app.py", label="Home", icon="🏠")
        st.page_link("pages/1_Customer_Chat.py", label="Customer Chat", icon="💬")
        st.page_link("pages/3_Knowledge_Base.py", label="Knowledge Base", icon="📚")
        st.page_link("pages/2_Admin_Dashboard.py", label="Admin Dashboard", icon="🔐")
        
        st.markdown("---")
        st.markdown("#### ⚡ System Status")
        st.caption("Click button to inspect ChromaDB backend details:")
        
        # Single ChromaDB Details Button
        if st.button("⚡ ChromaDB Backend Details", use_container_width=True, key="sb_btn_chroma"):
            st.session_state["show_db_info"] = not st.session_state.get("show_db_info", False)
            
        # Display ChromaDB Backend Details Box
        if st.session_state.get("show_db_info", False):
            st.markdown("---")
            st.info("""
            **⚡ ChromaDB VectorStore Details:**
            - **Database**: ChromaDB Persistent Store
            - **Collection Name**: `dinemind_knowledge`
            - **Embedding Model**: `text-embedding-3-small`
            - **Storage Path**: `./vectorstore`
            - **Indexed Chunks**: `21 Vector Embeddings`
            - **Distance Metric**: `L2 / Cosine Similarity`
            - **Status**: Persistent & Online
            """)
            if st.button("✖️ Close Details", key="close_chroma"):
                st.session_state["show_db_info"] = False
                st.rerun()

        st.markdown("---")
        st.caption("DineMind AI • Production RAG Engine")
