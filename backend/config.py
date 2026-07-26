import os
from pathlib import Path
from dotenv import load_dotenv

# Set ChromaDB telemetry off
os.environ["ANONYMIZED_TELEMETRY"] = "False"

# Load environment variables from .env if present
load_dotenv()

BASE_DIR = Path(__file__).parent.parent
DOCUMENTS_DIR = BASE_DIR / "documents"
UPLOADS_DIR = BASE_DIR / "uploads"
VECTORSTORE_DIR = BASE_DIR / "vectorstore"

# Ensure directories exist
DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)
VECTORSTORE_DIR.mkdir(parents=True, exist_ok=True)

# Default OpenRouter API Key placeholder
DEFAULT_OPENROUTER_KEY = "sk-or-v1-your_openrouter_api_key_here"

API_KEY = os.getenv("OPENAI_API_KEY") or os.getenv("OPENROUTER_API_KEY") or DEFAULT_OPENROUTER_KEY
IS_OPENROUTER = API_KEY.startswith("sk-or-")

if IS_OPENROUTER:
    OPENAI_API_BASE = "https://openrouter.ai/api/v1"
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "openai/gpt-4o-mini")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-small")
else:
    OPENAI_API_BASE = os.getenv("OPENAI_API_BASE", "https://api.openai.com/v1")
    LLM_MODEL_NAME = os.getenv("LLM_MODEL_NAME", "gpt-4o-mini")
    EMBEDDING_MODEL_NAME = os.getenv("EMBEDDING_MODEL_NAME", "text-embedding-3-small")

# RAG & Chunking Config
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 4
COLLECTION_NAME = "dinemind_knowledge"
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD", "admin123")
