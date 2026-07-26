import os
from pathlib import Path
import streamlit as st

from components.header import render_hero, load_css
from components.sidebar import render_sidebar
from components.cards import render_metric_card
from backend.rag.vectorstore import VectorStoreManager

st.set_page_config(
    page_title="Knowledge Base - DineMind AI",
    page_icon="📚",
    layout="wide"
)

# Load CSS & Sidebar
load_css()
render_sidebar()

# Initialize VectorStore Manager
if "vectorstore_mgr" not in st.session_state:
    st.session_state.vectorstore_mgr = VectorStoreManager()

vm = st.session_state.vectorstore_mgr
doc_list = vm.get_document_metadata_list()
stats = vm.get_stats()

# Header Banner
render_hero(
    title="Knowledge Base Repository",
    subtitle="View, preview, download, replace, or delete active restaurant documents in ChromaDB.",
    icon="📚"
)

# Metrics Summary Bar
m1, m2, m3, m4 = st.columns(4)
with m1:
    render_metric_card("Total Documents", str(stats["document_count"]), "PDF, CSV, TXT, MD")
with m2:
    render_metric_card("Vector Chunks", str(stats["chunk_count"]), "ChromaDB Collection")
with m3:
    render_metric_card("Index Health", "100% ONLINE", "Persistent Store")
with m4:
    render_metric_card("Last Refreshed", stats["last_updated"], "Live Timestamp")

st.markdown("---")
st.markdown("### 📄 Active Restaurant Documents")

if not doc_list:
    st.info("No documents currently present in the knowledge base.")
else:
    # Render table header
    h_col1, h_col2, h_col3, h_col4, h_col5, h_col6 = st.columns([2.5, 1.2, 1.0, 1.5, 1.0, 2.5])
    with h_col1:
        st.markdown("**File Name**")
    with h_col2:
        st.markdown("**Type**")
    with h_col3:
        st.markdown("**Size**")
    with h_col4:
        st.markdown("**Last Modified**")
    with h_col5:
        st.markdown("**Status**")
    with h_col6:
        st.markdown("**Actions**")
        
    st.markdown("<hr style='margin: 0.5rem 0 1rem 0; border-color: #CBD5E1;'>", unsafe_allow_html=True)

    # Render Document Rows
    for idx, doc in enumerate(doc_list):
        c1, c2, c3, c4, c5, c6 = st.columns([2.5, 1.2, 1.0, 1.5, 1.0, 2.5])
        
        with c1:
            st.markdown(f"📄 **{doc['filename']}**")
        with c2:
            st.caption(doc["file_type"])
        with c3:
            st.caption(doc["size_formatted"])
        with c4:
            st.caption(doc["upload_date"])
        with c5:
            st.markdown("<span class='badge-pill badge-mint'>Indexed</span>", unsafe_allow_html=True)
            
        with c6:
            btn_col1, btn_col2, btn_col3 = st.columns(3)
            
            # View Button
            with btn_col1:
                if st.button("👁️ View", key=f"view_{idx}", use_container_width=True):
                    st.session_state[f"preview_{doc['filename']}"] = True
                    
            # Download Button
            with btn_col2:
                if os.path.exists(doc["filepath"]):
                    with open(doc["filepath"], "rb") as f:
                        st.download_button(
                            label="📥 Get",
                            data=f,
                            file_name=doc["filename"],
                            mime="application/octet-stream",
                            key=f"dl_{idx}",
                            use_container_width=True
                        )
                        
            # Delete Button
            with btn_col3:
                if st.button("🗑️ Del", key=f"del_kb_{idx}", use_container_width=True):
                    vm.delete_document(doc["filename"])
                    st.success(f"Deleted {doc['filename']} and updated index.")
                    st.rerun()

        # Preview Expander / Replace Drawer if triggered
        if st.session_state.get(f"preview_{doc['filename']}", False):
            with st.expander(f"🔍 Inspect Content & Replace: {doc['filename']}", expanded=True):
                col_prev, col_rep = st.columns([2, 1])
                
                with col_prev:
                    st.markdown("##### Document Content Preview")
                    try:
                        if doc["filepath"].endswith(".pdf"):
                            from langchain_community.document_loaders import PyPDFLoader
                            loader = PyPDFLoader(doc["filepath"])
                            pages = loader.load()
                            text_preview = "\n\n".join([p.page_content for p in pages[:3]])
                            st.text_area("Preview (First 3 pages)", text_preview, height=200)
                        else:
                            with open(doc["filepath"], "r", encoding="utf-8", errors="ignore") as f:
                                st.text_area("File Content", f.read()[:3000], height=200)
                    except Exception as e:
                        st.error(f"Error reading file: {e}")
                        
                with col_rep:
                    st.markdown("##### Replace Document")
                    new_file = st.file_uploader(f"Upload new replacement for {doc['filename']}", key=f"rep_file_{idx}")
                    if new_file:
                        if st.button("Confirm Replace", key=f"conf_rep_{idx}", type="primary"):
                            vm.replace_document(doc["filename"], new_file, doc["filename"])
                            st.success(f"Replaced {doc['filename']} and re-indexed ChromaDB!")
                            st.session_state[f"preview_{doc['filename']}"] = False
                            st.rerun()
                            
                if st.button("Close Preview", key=f"close_{idx}"):
                    st.session_state[f"preview_{doc['filename']}"] = False
                    st.rerun()
                    
        st.markdown("<hr style='margin: 0.5rem 0; border-color: #E2E8F0;'>", unsafe_allow_html=True)
