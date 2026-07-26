import os
from pathlib import Path
from typing import List
from langchain_core.documents import Document
from langchain_community.document_loaders import PyPDFLoader, CSVLoader, TextLoader

def load_single_document(file_path: str) -> List[Document]:
    """Loads a single document based on its extension (PDF, CSV, TXT, Markdown)."""
    path = Path(file_path)
    ext = path.suffix.lower()
    
    if ext == ".pdf":
        loader = PyPDFLoader(str(path))
        docs = loader.load()
    elif ext == ".csv":
        loader = CSVLoader(str(path), encoding="utf-8")
        docs = loader.load()
    elif ext in [".txt", ".md", ".markdown"]:
        loader = TextLoader(str(path), encoding="utf-8")
        docs = loader.load()
    else:
        raise ValueError(f"Unsupported file format: {ext}")
        
    # Inject source metadata for UI tracking
    for doc in docs:
        doc.metadata["filename"] = path.name
        doc.metadata["file_type"] = ext
        
    return docs

def load_all_documents_from_directory(directory_path: str) -> List[Document]:
    """Loads all supported documents (.pdf, .csv, .txt, .md) from a directory."""
    dir_path = Path(directory_path)
    all_docs = []
    
    if not dir_path.exists():
        return all_docs
        
    for item in dir_path.glob("*"):
        if item.suffix.lower() in [".pdf", ".csv", ".txt", ".md", ".markdown"]:
            try:
                docs = load_single_document(str(item))
                all_docs.extend(docs)
            except Exception as e:
                print(f"Error loading {item.name}: {e}")
                
    return all_docs
