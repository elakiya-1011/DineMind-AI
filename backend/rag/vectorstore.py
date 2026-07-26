import sys
import shutil
import time
import os
from typing import List, Tuple, Dict, Any
from pathlib import Path

# Environment overrides for ChromaDB local Segment API
os.environ["ANONYMIZED_TELEMETRY"] = "False"
os.environ["CHROMA_API_IMPL"] = "chromadb.api.segment.SegmentAPI"

# Override sqlite3 with pysqlite3 for Linux / Streamlit Cloud compatibility
try:
    __import__('pysqlite3')
    sys.modules['sqlite3'] = sys.modules.pop('pysqlite3')
except Exception:
    pass

from langchain_core.documents import Document
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

from backend.config import (
    VECTORSTORE_DIR, DOCUMENTS_DIR, UPLOADS_DIR,
    API_KEY, OPENAI_API_BASE, EMBEDDING_MODEL_NAME, COLLECTION_NAME, TOP_K_RESULTS
)
from backend.rag.loader import load_all_documents_from_directory, load_single_document
from backend.rag.splitter import split_documents
from backend.utils.generator import generate_default_documents

def get_embedding_function():
    """Initializes lightweight OpenAI / OpenRouter embedding function for cloud deployment."""
    is_placeholder = "your_openrouter" in API_KEY or "your_openai" in API_KEY or len(API_KEY) < 15
    
    if not is_placeholder:
        try:
            return OpenAIEmbeddings(
                api_key=API_KEY,
                openai_api_base=OPENAI_API_BASE,
                model=EMBEDDING_MODEL_NAME
            )
        except Exception as e:
            print(f"Warning: OpenAIEmbeddings init failed ({e})")
            
    try:
        from langchain_community.embeddings import FakeEmbeddings
        return FakeEmbeddings(size=1536)
    except Exception:
        return OpenAIEmbeddings(api_key=API_KEY, openai_api_base=OPENAI_API_BASE, model=EMBEDDING_MODEL_NAME)

class VectorStoreManager:
    """Manages ChromaDB vector store initialization, document indexing, CRUD, and rebuilds."""
    
    def __init__(self):
        self.embedding_fn = get_embedding_function()
        self.vectorstore_dir = str(VECTORSTORE_DIR)
        self.vectorstore = None
        self._init_vectorstore()
        
    def _init_vectorstore(self):
        """Initializes ChromaDB client safely for both local and Streamlit Cloud environments."""
        try:
            import chromadb
            client = chromadb.PersistentClient(path=self.vectorstore_dir)
            self.vectorstore = Chroma(
                client=client,
                collection_name=COLLECTION_NAME,
                embedding_function=self.embedding_fn
            )
        except Exception as e:
            print(f"Chroma PersistentClient fallback due to: {e}")
            self.vectorstore = Chroma(
                collection_name=COLLECTION_NAME,
                embedding_function=self.embedding_fn,
                persist_directory=self.vectorstore_dir
            )
            
        try:
            if self.vectorstore._collection.count() == 0:
                self.index_all_documents()
        except Exception:
            self.index_all_documents()
        
    def get_stats(self) -> dict:
        """Returns knowledge base overview statistics."""
        try:
            count = self.vectorstore._collection.count()
        except Exception:
            count = 0
            
        doc_files = set()
        for d in [DOCUMENTS_DIR, UPLOADS_DIR]:
            if d.exists():
                for f in d.glob("*"):
                    if f.suffix.lower() in [".pdf", ".csv", ".txt", ".md", ".markdown"]:
                        doc_files.add(f.name)
                        
        last_updated = time.strftime("%Y-%m-%d %H:%M:%S")
        return {
            "chunk_count": count,
            "document_count": len(doc_files),
            "documents": list(doc_files),
            "last_updated": last_updated
        }

    def get_document_metadata_list(self) -> List[Dict[str, Any]]:
        """Returns detailed metadata for all available documents."""
        generate_default_documents()
        doc_list = []
        
        seen_filenames = set()
        for folder in [DOCUMENTS_DIR, UPLOADS_DIR]:
            if not folder.exists():
                continue
            for f in folder.glob("*"):
                ext = f.suffix.lower()
                if ext in [".pdf", ".csv", ".txt", ".md", ".markdown"]:
                    if f.name in seen_filenames:
                        continue
                    seen_filenames.add(f.name)
                    
                    file_size_bytes = f.stat().st_size
                    if file_size_bytes < 1024:
                        size_str = f"{file_size_bytes} B"
                    elif file_size_bytes < 1024 * 1024:
                        size_str = f"{round(file_size_bytes / 1024, 1)} KB"
                    else:
                        size_str = f"{round(file_size_bytes / (1024 * 1024), 2)} MB"
                        
                    mod_time = time.strftime("%Y-%m-%d %H:%M", time.localtime(f.stat().st_mtime))
                    
                    file_type_map = {
                        ".pdf": "PDF Document",
                        ".csv": "CSV Spreadsheet",
                        ".txt": "Text File",
                        ".md": "Markdown",
                        ".markdown": "Markdown"
                    }
                    
                    doc_list.append({
                        "filename": f.name,
                        "file_type": file_type_map.get(ext, ext.upper()),
                        "size_formatted": size_str,
                        "upload_date": mod_time,
                        "status": "Indexed",
                        "filepath": str(f)
                    })
                    
        return doc_list

    def index_all_documents(self):
        """Indexes all default documents and uploaded files into ChromaDB."""
        generate_default_documents()
        docs = load_all_documents_from_directory(str(DOCUMENTS_DIR))
        upload_docs = load_all_documents_from_directory(str(UPLOADS_DIR))
        docs.extend(upload_docs)
        
        if not docs:
            return 0
            
        chunks = split_documents(docs)
        try:
            import chromadb
            client = chromadb.PersistentClient(path=self.vectorstore_dir)
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding_fn,
                collection_name=COLLECTION_NAME,
                client=client
            )
        except Exception:
            self.vectorstore = Chroma.from_documents(
                documents=chunks,
                embedding=self.embedding_fn,
                collection_name=COLLECTION_NAME,
                persist_directory=self.vectorstore_dir
            )
        return len(chunks)

    def rebuild_index(self):
        """Wipes and completely rebuilds the vector index from scratch."""
        try:
            self.vectorstore.delete_collection()
        except Exception:
            pass
            
        if VECTORSTORE_DIR.exists():
            try:
                shutil.rmtree(str(VECTORSTORE_DIR))
            except Exception as e:
                print(f"Directory cleanup warning: {e}")
                
        VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)
        self._init_vectorstore()
        return self.index_all_documents()

    def add_document(self, file_path: str):
        """Indexes a single new document into ChromaDB."""
        docs = load_single_document(file_path)
        chunks = split_documents(docs)
        self.vectorstore.add_documents(chunks)
        return len(chunks)

    def delete_document(self, filename: str) -> bool:
        """Deletes physical file and re-indexes remaining files in ChromaDB."""
        deleted = False
        for folder in [UPLOADS_DIR, DOCUMENTS_DIR]:
            target = folder / filename
            if target.exists():
                try:
                    target.unlink()
                    deleted = True
                except Exception as e:
                    print(f"Error deleting file {filename}: {e}")
                    
        if deleted:
            self.rebuild_index()
            return True
        return False

    def replace_document(self, filename: str, new_file_buffer, new_filename: str = None) -> bool:
        """Replaces an existing document with a new upload buffer and updates vector index."""
        target_name = new_filename or filename
        self.delete_document(filename)
        
        save_path = UPLOADS_DIR / target_name
        with open(save_path, "wb") as f:
            f.write(new_file_buffer.getbuffer())
            
        self.add_document(str(save_path))
        return True

    def similarity_search_with_score(self, query: str, top_k: int = TOP_K_RESULTS) -> List[Tuple[Document, float]]:
        """Performs vector similarity search with safe runtime exception handling."""
        try:
            if self.vectorstore._collection.count() == 0:
                self.index_all_documents()
        except Exception:
            self.index_all_documents()
            
        start_t = time.time()
        results = self.vectorstore.similarity_search_with_score(query, k=top_k)
        elapsed_ms = round((time.time() - start_t) * 1000, 2)
        return results, elapsed_ms
