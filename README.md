# 🍽️ DineMind AI

> **AI-Powered Restaurant Customer Assistant using LangChain, RAG, and AI Orchestration**

DineMind AI is a production-ready, enterprise-grade AI web application designed to serve as an intelligent Customer Concierge and simulated food ordering system for modern restaurants. Built using **Streamlit**, **LangChain (LCEL)**, **OpenAI / OpenRouter**, and **ChromaDB**, it features strict **anti-hallucination guardrails**, a **Knowledge Base Repository**, an **Admin Control Hub**, and simulated **Session Food Ordering**.

---

## 🌟 Key Features

- **💬 Expanded Customer Assistant & Cart System**: Interactive natural language interface supporting greetings, general QA, menu recommendations, allergy checks, and simulated food ordering commands (`"Add 1 Margherita Pizza"`, `"Show my cart"`, `"Place my order"`).
- **🛡️ Zero-Hallucination Guardrail**: Employs a post-generation **Self-Reflection Audit** chain to guarantee responses are 100% grounded in official restaurant documents. If data is missing, it safely fallbacks with a polite disclaimer.
- **📚 Dedicated Knowledge Base Page**: Interactive document repository displaying all active restaurant files (`Menu.pdf`, `Restaurant_FAQ.pdf`, `Delivery_Policy.pdf`, `Restaurant_Policies.pdf`, `Offers.pdf`, `Ingredients.csv`, etc.) with file attributes (Name, Type, Size, Upload Date, Index Status) and action buttons (**View**, **Download**, **Delete**, **Replace**).
- **🔐 Redesigned Admin Operations Hub**: Password-protected portal (`Username: admin | Password: admin123`) providing document uploads (PDF, CSV, TXT, MD), document replacement, deletion, and one-click ChromaDB index rebuilding.
- **🎨 High-Contrast Pastel UI**: Overhauled CSS design system ensuring ultra-sharp text legibility and dark slate contrast across both Streamlit Light and Dark browser themes.

---

## 📂 Project Structure

```text
dinemind_ai/
│
├── app.py                      # Main entry point & home landing page
├── pages/                      # Multi-page application views
│   ├── 1_Customer_Chat.py       # Customer assistant & simulated ordering
│   ├── 2_Admin_Dashboard.py     # Admin authentication & operations hub
│   └── 3_Knowledge_Base.py      # Dedicated Knowledge Base document repository
│
├── components/                 # Reusable Streamlit UI components
│   ├── header.py               # Gradient hero banner component
│   ├── sidebar.py              # System status & navigation sidebar
│   └── cards.py               # High contrast metric boxes & feature cards
│
├── backend/                    # Core Python AI & RAG engine
│   ├── config.py               # Environment configuration & API key settings
│   ├── rag/                    # Ingestion & ChromaDB vectorstore pipeline
│   │   ├── loader.py           # Multi-format document loaders (PDF, CSV, TXT, MD)
│   │   ├── splitter.py         # RecursiveCharacterTextSplitter wrapper
│   │   └── vectorstore.py      # ChromaDB manager with metadata list & CRUD
│   ├── prompts/                # Prompt Engineering templates
│   │   ├── system_prompts.py   # Role, Contextual, CoT, & Reflection prompts
│   │   └── few_shot_examples.py# Few-shot exemplars & ReAct examples
│   ├── chains/                 # LangChain LCEL runnable chains
│   │   ├── router.py           # Intent classification router
│   │   ├── reflection_chain.py # Self-reflection audit chain
│   │   └── rag_chain.py        # Master RAG orchestrator with Cart Parser
│   ├── memory/                 # Conversation memory manager
│   │   └── chat_memory.py      # Transcript history tracker
│   └── utils/                  # Telemetry & document utilities
│       ├── tracer.py           # Execution telemetry recorder
│       └── generator.py        # Synthetic default document generator
│
├── assets/                     # UI Assets & Styling
│   └── style.css               # High-contrast pastel CSS design system
├── documents/                  # Storage for default synthetic restaurant files
├── uploads/                    # Storage for admin uploaded custom files
├── vectorstore/                # ChromaDB local persistent directory
├── .env.example                # Environment variables template
├── .gitignore                  # Git ignore rules
├── LICENSE                     # MIT License
├── README.md                   # Application documentation
└── requirements.txt            # Python dependencies
```

---

## 🛠️ Technology Stack

| Layer | Technology |
|---|---|
| **Frontend UI** | Streamlit, Custom High-Contrast Pastel CSS |
| **Orchestration** | LangChain, LCEL (LangChain Expression Language) |
| **LLM Provider** | OpenAI API / OpenRouter (`gpt-4o-mini`) |
| **Embeddings** | OpenAI Embeddings (`text-embedding-3-small`) / HuggingFace |
| **Vector DB** | ChromaDB Persistent Store |
| **Document Loaders** | PyPDF, CSVLoader, TextLoader |

---

## 🚀 Quick Start Guide

### 1. Installation & Setup

```bash
cd dinemind_ai
pip install -r requirements.txt
```

### 2. Environment Variables Setup
Create `.env`:
```env
OPENAI_API_KEY=your_openrouter_or_openai_api_key_here
LLM_MODEL_NAME=openai/gpt-4o-mini
ADMIN_PASSWORD=admin123
```

### 3. Run Application

```bash
streamlit run app.py
```
App will start at `http://localhost:8501`.

---

## 🔑 Default Admin Credentials

- **Username**: `admin`
- **Password**: `admin123`

---

## 📜 License

Distributed under the [MIT License](file:///C:/Users/Pranavikha/.gemini/antigravity/scratch/dinemind_ai/LICENSE).
