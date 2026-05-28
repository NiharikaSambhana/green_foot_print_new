import streamlit as st

st.set_page_config(
    page_title="GreenPrompt AI",
    page_icon="🌱",
    layout="wide"
)

# -------------------------------------
# SIDEBAR
# -------------------------------------

st.sidebar.image(
    "assets/tcs_logo.png",
    width=150
)

st.sidebar.title(
    "GreenPrompt AI"
)

menu = st.sidebar.radio(
    "Navigation",
    [
        "🏠 Home",
        "📄 Document Processing",
        "🧠 Embeddings & Vector DB",
        "🔍 Semantic Retrieval",
        "🤖 RAG Chatbot",
        "📊 Dashboard",
        "ℹ️ Team"
    ]
)

# -------------------------------------
# HOME
# -------------------------------------

if menu == "🏠 Home":

    st.title(
        "🌱 GreenPrompt AI"
    )

    st.subheader(
        "Enterprise AI Sustainability Assistant"
    )

    st.markdown("---")

    c1, c2 = st.columns(2)

    with c1:

        st.info("""
        Project Goal

        Analyze enterprise AI usage

        Measure sustainability impact

        Reduce carbon emissions

        Improve model selection

        Build responsible AI workflows
        """)

    with c2:

        st.success("""
        Technologies

        ✔ LangChain

        ✔ ChromaDB

        ✔ OpenAI Embeddings

        ✔ RAG

        ✔ Streamlit

        ✔ Responsible AI

        ✔ Guardrails

        ✔ Explainable AI
        """)

# -------------------------------------
# DOCUMENT PROCESSING
# -------------------------------------

elif menu == "📄 Document Processing":

    st.title(
        "📄 Chunking Pipeline"
    )

    st.markdown("---")

    st.write("Status")

    st.success("✔ Documents Loaded")

    st.success("✔ TXT Support")

    st.success("✔ CSV Support")

    st.success("✔ LOG Support")

    st.success("✔ Metadata Added")

    st.success("✔ Chunking Completed")

    st.metric(
        "Chunk Size",
        "1000"
    )

    st.metric(
        "Chunk Overlap",
        "200"
    )

# -------------------------------------
# EMBEDDING
# -------------------------------------

elif menu == "🧠 Embeddings & Vector DB":

    st.title(
        "🧠 Embedding Pipeline"
    )

    st.markdown("---")

    st.success(
        "Embedding Model Loaded"
    )

    st.code(
        "azure/genailab-maas-text-embedding-3-large"
    )

    st.success(
        "ChromaDB Created"
    )

    st.success(
        "Embeddings Stored"
    )

    st.success(
        "Metadata Indexed"
    )

# -------------------------------------
# RETRIEVAL
# -------------------------------------

elif menu == "🔍 Semantic Retrieval":

    st.title(
        "🔍 Semantic Search"
    )

    st.markdown("---")

    st.write("""
    User Query
        ↓
    Convert to Embedding
        ↓
    Similarity Search
        ↓
    Retrieve Relevant Chunks
        ↓
    Send Context to LLM
    """)

    st.info("""
    Current Features

    ✔ Similarity Search

    ✔ Confidence Score

    ✔ Metadata Tracking

    ✔ Top-k Retrieval
    """)

# -------------------------------------
# CHATBOT
# -------------------------------------

elif menu == "🤖 RAG Chatbot":

    st.title(
        "🤖 Enterprise Sustainability Chatbot"
    )

    st.warning(
        "Integration Pending"
    )

    question = st.text_input(
        "Ask a question"
    )

    if question:

        st.info(
            "RAG response will appear here after integration."
        )

# -------------------------------------
# DASHBOARD
# -------------------------------------

elif menu == "📊 Dashboard":

    st.title(
        "📊 Analytics Dashboard"
    )

    st.warning(
        "Dashboard integration pending from Team Member 4"
    )

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Documents",
        "5"
    )

    c2.metric(
        "Chunks",
        "6"
    )

    c3.metric(
        "Vector DB",
        "Ready"
    )

# -------------------------------------
# TEAM
# -------------------------------------

elif menu == "ℹ️ Team":

    st.title(
        "👥 Team GreenPrompt"
    )

    st.markdown("---")

    st.subheader(
        "Project Modules"
    )

    st.write("""
    Member 1

    Chunking

    Embeddings

    ChromaDB

    Semantic Retrieval

    Confidence Score
    """)

    st.write("""
    Member 2

    RAG

    Guardrails

    LLM Integration

    Summarization
    """)

    st.write("""
    Member 3

    Carbon Engine

    Emission Calculations

    Sustainability Metrics
    """)

    st.write("""
    Member 4

    Streamlit Dashboard

    Analytics

    Charts

    User Interface
    """)
