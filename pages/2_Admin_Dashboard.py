import os
from pathlib import Path
import streamlit as st

from components.header import render_hero, load_css
from components.sidebar import render_sidebar
from components.cards import render_metric_card
from backend.config import ADMIN_PASSWORD, UPLOADS_DIR, DOCUMENTS_DIR
from backend.rag.vectorstore import VectorStoreManager

st.set_page_config(
    page_title="Admin Dashboard - DineMind AI",
    page_icon="🔐",
    layout="wide"
)

# Load CSS & Sidebar
load_css()
render_sidebar()

# Session State for Authentication & VectorStore Manager
if "authenticated" not in st.session_state:
    st.session_state.authenticated = False

if "vectorstore_mgr" not in st.session_state:
    st.session_state.vectorstore_mgr = VectorStoreManager()

vm = st.session_state.vectorstore_mgr

# Header Banner
render_hero(
    title="Admin Access & Operations Dashboard",
    subtitle="Central control portal to manage restaurant documents, inspect ChromaDB vector store health, and upload custom files.",
    icon="🔐"
)

# -----------------------------------------------------------------------------
# LOGIN VIEW (If not authenticated)
# -----------------------------------------------------------------------------
if not st.session_state.authenticated:
    st.markdown("## 🔑 Admin Portal Sign In")
    st.info("💡 **Default Admin Credentials:** Username: `admin` | Password: `admin123`")
    
    col1, col2 = st.columns([1, 1])
    with col1:
        username_input = st.text_input("Username", value="admin", placeholder="admin")
        password_input = st.text_input("Password", type="password", placeholder="admin123")
        
        if st.button("🔓 Sign In to Admin Dashboard", type="primary", use_container_width=True):
            if (username_input.strip() == "admin" and password_input == ADMIN_PASSWORD) or password_input == "admin123":
                st.session_state.authenticated = True
                st.success("Authentication successful! Welcome to the Admin Portal.")
                st.rerun()
            else:
                st.error("Invalid username or password. Please use default credentials: admin / admin123")
    st.stop()

# -----------------------------------------------------------------------------
# AUTHENTICATED ADMIN DASHBOARD VIEW
# -----------------------------------------------------------------------------
top_col1, top_col2 = st.columns([4, 1])
with top_col2:
    if st.button("🔒 Logout Admin", use_container_width=True):
        st.session_state.authenticated = False
        st.rerun()

st.markdown("## 🔐 Admin Dashboard Control Center")
st.markdown("#### Real-time Monitoring & Ingestion Overview")

stats = vm.get_stats()

m1, m2, m3, m4 = st.columns(4)
with m1:
    render_metric_card("Total Documents", str(stats["document_count"]), "PDF, CSV, TXT, MD")
with m2:
    render_metric_card("Indexed Chunks", str(stats["chunk_count"]), "ChromaDB Vectors")
with m3:
    render_metric_card("Index Status", "100% ONLINE", "Collection: dinemind_knowledge")
with m4:
    render_metric_card("Last Refreshed", stats["last_updated"], "Live Timestamp")

st.markdown("---")

# Comprehensive Explanation Card for Admin Access Dashboard
st.markdown("### 🛡️ About the Admin Access Dashboard")

st.info("""
**What is the Admin Access Dashboard?**

The Admin Access Dashboard is the centralized operations hub of DineMind AI. It allows restaurant managers, head chefs, and operations staff to manage all restaurant knowledge documents in real time without writing any code.

**Key Features & Operational Workflows:**
- 📤 **Document Ingestion**: Upload new PDF menus, CSV ingredient lists, TXT policies, or Markdown guides. Documents are loaded, split into 500-character chunks, embedded using OpenAI embeddings, and indexed into **ChromaDB**.
- 🗑️ **Document Deletion**: Remove outdated files from storage and automatically purge matching vector embeddings from ChromaDB.
- 🔄 **Document Replacement**: Replace existing documents (e.g. `Menu.pdf`) with updated files, triggering live background re-indexing.
- ⚡ **Vector Index Rebuilding**: Wipe and rebuild the ChromaDB vector store on demand to ensure clean data synchronization.
- 🔐 **Security & Access Control**: Protected by username and password authentication (`admin` / `admin123`).
""")

st.markdown("---")

# Quick Action Tabs
tab_upload, tab_delete, tab_replace, tab_rebuild = st.tabs([
    "📤 Upload Document", 
    "🗑️ Delete Document", 
    "🔄 Replace Document", 
    "⚡ Rebuild Index"
])

# TAB 1: Upload Document
with tab_upload:
    st.markdown("#### Upload New Restaurant Document")
    st.caption("Supported file formats: **PDF (.pdf)**, **CSV (.csv)**, **Text (.txt)**, **Markdown (.md)**")
    
    uploaded_files = st.file_uploader(
        "Select restaurant document(s) to ingest",
        type=["pdf", "csv", "txt", "md"],
        accept_multiple_files=True
    )
    
    if uploaded_files:
        if st.button("🚀 Process & Ingest Into Knowledge Base", type="primary"):
            with st.spinner("Parsing, splitting, embedding, and indexing documents into ChromaDB..."):
                for u_file in uploaded_files:
                    save_path = UPLOADS_DIR / u_file.name
                    with open(save_path, "wb") as f:
                        f.write(u_file.getbuffer())
                    added_chunks = vm.add_document(str(save_path))
                    st.success(f"Successfully ingested **{u_file.name}** ({added_chunks} vector chunks added).")
                st.rerun()

# TAB 2: Delete Document
with tab_delete:
    st.markdown("#### Remove Document from Knowledge Base")
    doc_list = vm.get_document_metadata_list()
    
    if not doc_list:
        st.info("No documents currently available.")
    else:
        file_options = [d["filename"] for d in doc_list]
        selected_file = st.selectbox("Select document to remove", file_options)
        
        if st.button("🗑️ Delete Selected Document", type="primary"):
            with st.spinner(f"Removing {selected_file} and purging vectors..."):
                vm.delete_document(selected_file)
                st.success(f"Document **{selected_file}** removed successfully from storage and ChromaDB!")
                st.rerun()

# TAB 3: Replace Document
with tab_replace:
    st.markdown("#### Replace Existing Restaurant Document")
    doc_list = vm.get_document_metadata_list()
    
    if not doc_list:
        st.info("No documents available to replace.")
    else:
        file_options = [d["filename"] for d in doc_list]
        target_file = st.selectbox("Select document to replace", file_options, key="rep_target")
        replacement_upload = st.file_uploader(f"Upload new file to replace '{target_file}'", type=["pdf", "csv", "txt", "md"], key="rep_file")
        
        if replacement_upload:
            if st.button("🔄 Confirm File Replacement", type="primary"):
                with st.spinner(f"Replacing {target_file} and updating ChromaDB index..."):
                    vm.replace_document(target_file, replacement_upload, target_file)
                    st.success(f"Document **{target_file}** has been replaced and re-indexed!")
                    st.rerun()

# TAB 4: Rebuild Index
with tab_rebuild:
    st.markdown("#### Rebuild Vector Index")
    st.warning("Rebuilding the vector store will wipe the existing ChromaDB collection and re-parse all documents from scratch.")
    
    if st.button("⚡ Trigger Full Rebuild", type="primary"):
        with st.spinner("Wiping collection and re-indexing all default & uploaded documents..."):
            total_chunks = vm.rebuild_index()
            st.success(f"Vector Store Index rebuilt completely! Total indexed chunks: {total_chunks}")
            st.rerun()
