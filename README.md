LogRAG is a local, secure Retrieval-Augmented Generation (RAG) system that helps engineers understand, diagnose, and resolve production issues by analyzing historical logs and generating structured explanations using a local Large Language Model (LLM).

The system leverages the Endee vector database for efficient storage and retrieval of log embeddings, enabling fast semantic search across large volumes of historical logs. By combining Endee’s high-performance vector indexing with local LLM reasoning, LogRAG delivers accurate and context-aware incident analysis while maintaining data privacy.

The system is designed to remain partially functional even when the LLM backend is unavailable, making it resilient and production-aware.







🚀 Key Features


🔍 Semantic Log Search using vector embeddings stored in Endee vector database


🗄️ High-performance vector indexing powered by Endee for scalable retrieval


🧠 LLM-powered log explanation (local, private via Ollama)


🛡️ Prompt-injection resistant by design


🧩 Graceful degradation when the LLM is unavailable (retrieval still works)








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


🏗️ System Architecture 

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


🛡️ Security Considerations

Logs and user input are treated as untrusted data

Prompt-injection patterns are sanitized

LLM instructions cannot be overridden by logs

No external API calls required (local-first design)

Ideal Use Cases

DevOps troubleshooting

SRE incident response

Log exploration during outages

Interview/demo projects

Local AI experimentation


🧠 Summary

LogRAG combines semantic search, local LLMs, and resilient system design to create a powerful log analysis tool that prioritizes privacy, reliability, and explainability.

This project demonstrates real-world application of:

Retrieval-Augmented Generation

Failure-aware system design

Practical ML + backend integration





