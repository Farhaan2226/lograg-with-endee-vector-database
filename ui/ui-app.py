import streamlit as st
import requests

# ---------------- CONFIG ----------------

API_URL = "http://lograg-api:8000/explain"


# ---------------- PAGE SETUP ----------------

st.set_page_config(
    page_title="LogRAG",
    page_icon="🛠️",
    layout="centered"
)

# ---------------- STYLES ----------------

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #020617, #0f172a);
    color: white;
}

/* Force white text everywhere */
html, body, [class*="css"] {
    color: #ffffff !important;
}

/* Text area */
textarea {
    background-color: #020617 !important;
    color: #ffffff !important;
    border-radius: 12px !important;
    border: 1px solid #334155 !important;
}

/* Button */
button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    border: none !important;
}
button:hover {
    background: linear-gradient(135deg, #1e40af, #1e3a8a) !important;
}

/* Cards */
.card {
    background: linear-gradient(135deg, #020617, #0f172a);
    padding: 20px;
    border-radius: 16px;
    border: 1px solid #334155;
    margin-bottom: 16px;
    box-shadow: 0 10px 30px rgba(0,0,0,0.35);
}

/* Titles */
.section-title {
    font-size: 20px;
    font-weight: 700;
    margin-bottom: 12px;
    color: #e5e7eb;
}

/* Metadata labels */
.meta {
    color: #93c5fd;
    font-weight: 600;
}

/* Metadata values */
.value {
    color: #ffffff;
    font-weight: 500;
}

/* LLM status */
.status-ok {
    background: linear-gradient(135deg, #065f46, #047857);
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #10b981;
    font-weight: 600;
    margin-bottom: 16px;
}

.status-warn {
    background: linear-gradient(135deg, #78350f, #92400e);
    padding: 14px;
    border-radius: 14px;
    border: 1px solid #f59e0b;
    font-weight: 600;
    margin-bottom: 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------

st.markdown("## 🛠️ LogRAG – Explain My Logs")
st.markdown(
    "Analyze production logs using **semantic search + a local LLM** to identify root causes and fixes."
)

# ---------------- INPUT ----------------

query = st.text_area(
    "🔍 Enter error log or issue description",
    height=160,
    placeholder="Example: Auth service keeps crashing with exit code 137"
)

# ---------------- ACTION ----------------

if st.button("Explain issue 🚀"):

    if not query.strip():
        st.warning("Please enter a log or issue description.")
    else:
        with st.spinner("Analyzing logs and generating explanation…"):
            try:
                response = requests.post(
                    API_URL,
                    json={"query": query},
                    timeout=120
                )

                if response.status_code != 200:
                    st.error("Backend error")
                    st.code(response.text)
                else:
                    data = response.json()

                    llm_used = data.get("llm_used", False)
                    explanation = data.get("llm_explanation", "")
                    similar_logs = data.get("similar_logs", [])
                    reason = data.get("reason", "")

                    

                    # -------- AI EXPLANATION --------

                    if explanation:
                        st.markdown("""
                        <div class="card">
                            <div class="section-title">📌 AI Incident Analysis</div>
                        """ + explanation.replace("\n", "<br>") + """
                        </div>
                        """, unsafe_allow_html=True)

                    elif not llm_used:
                        st.markdown("""
                        <div class="card">
                            <div class="section-title">📌 Explanation unavailable</div>
                            LLM is currently offline. Relevant historical logs are shown below.
                        </div>
                        """, unsafe_allow_html=True)

                    # -------- RELEVANT LOGS --------

                    if similar_logs:
                        st.markdown("### 📄 Relevant Historical Logs")

                        for log in similar_logs:
                            meta = log.get("metadata", {})
                            score = log.get("score", 0)

                            st.markdown(f"""
                            <div class="card">
                                <div><span class="meta">Service:</span>
                                <span class="value"> {meta.get("service", "N/A")}</span></div>

                                <div><span class="meta">Level:</span>
                                <span class="value"> {meta.get("level", "N/A")}</span></div>

                                <div><span class="meta">Timestamp:</span>
                                <span class="value"> {meta.get("timestamp", "N/A")}</span></div>

                                <div><span class="meta">Similarity score:</span>
                                <span class="value"> {round(score, 3)}</span></div>
                            </div>
                            """, unsafe_allow_html=True)

            except requests.exceptions.ConnectionError:
                st.error("API not reachable. Is FastAPI running?")
            except requests.exceptions.Timeout:
                st.error("Request timed out. LLM may be busy.")
            except Exception as e:
                st.error("Unexpected error")
                st.exception(e)

# ---------------- FOOTER ----------------

st.markdown("""
<br>
<small style="color:#94a3b8">
FastAPI · SentenceTransformers · Ollama · Secure Local RAG
</small>
""", unsafe_allow_html=True)
