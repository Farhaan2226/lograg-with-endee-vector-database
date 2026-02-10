LogRAG is a local, secure Retrieval-Augmented Generation (RAG) system that helps engineers understand, diagnose, and resolve production issues by analyzing historical logs and generating structured explanations using a local Large Language Model (LLM).

The system is designed to remain partially functional even when the LLM backend is unavailable, making it resilient and production-aware.

🚀 Key Features

🔍 Semantic Log Search using vector embeddings

🧠 LLM-powered log explanation (local, private)

🛡️ Prompt-injection resistant by design

🧩 Graceful degradation when LLM is unavailable

📊 Streamlit UI for interactive analysis

🐳 Dockerized backend for reproducibility

🧪 Synthetic + real log ingestion support

🧠 What Problem Does LogRAG Solve?

Traditional log search relies on:

Exact keyword matches

Manual inspection

Fragmented context across services

LogRAG enables:

Meaning-based log retrieval

Cross-service correlation

Natural-language explanations of failures

🏗️ System Architecture (High Level)
User (Streamlit UI) --> Semantic Search (Sentence Transformers) --> Top-K Relevant Logs --> Structured Explanation / RAG results + reason (Ollama (Local LLM))

🧱 Technology Stack & Responsibilities
🎨 Frontend

Streamlit

Interactive web UI

Accepts log/error input

Displays:

LLM explanation

Similar historical logs

Fallback indicators

⚙️ Backend API

FastAPI

REST API for:

/search → semantic log retrieval

/explain → RAG + LLM explanation

/health → system status

Handles:

Input sanitization

Graceful LLM fallback

Secure prompt construction

🧠 Embedding Layer

SentenceTransformers

Model: all-MiniLM-L6-v2

Converts logs into dense semantic vectors

Enables similarity search beyond keywords

📐 Vector Similarity

Scikit-learn (Cosine Similarity)

Computes semantic similarity between:

User query

Stored log vectors

Retrieves Top-K relevant logs

🤖 LLM Engine

Ollama

Runs LLMs locally (e.g., mistral)

No cloud dependency

Ensures privacy & compliance

Used only after retrieval (RAG pattern)

🧪 Log Corpus

Synthetic + Real Logs

Synthetic logs simulate:

Application errors

Container failures

Network issues

Security events

Easily extensible to:

HDFS logs

OpenStack logs

Syslog

Web server logs

🐳 Containerization

Docker & Docker Compose

Isolates:

API

UI

Enables reproducible deployment

Simplifies local testing

🔄 Retrieval-Augmented Generation (RAG) Flow

User submits an issue or log snippet

Query is embedded using SentenceTransformers

Similar logs are retrieved from vector store

Retrieved logs are passed as untrusted context

LLM generates:

Root cause

Impact

Suggested fix

If LLM fails:

System returns semantic results only

Explains degradation reason



