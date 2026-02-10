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

What Problem Does LogRAG Solve?

Traditional log search relies on:

Exact keyword matches

Manual inspection

Fragmented context across services

LogRAG enables:

Meaning-based log retrieval

Cross-service correlation

Natural-language explanations of failures


User (Streamlit UI) --> Semantic Search (Sentence Transformers) --> Top-K Relevant Logs --> Structured Explanation / RAG results + reason (Ollama (Local LLM))


