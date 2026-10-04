"""Streamlit web app for the RAG Documentation Assistant."""

import streamlit as st
from src.pipeline import RAGPipeline
from configs.config import AppConfig

st.set_page_config(page_title="RAG Documentation Assistant", page_icon="📚", layout="wide")


@st.cache_resource
def load_pipeline():
    """Initialize and cache the RAG pipeline."""
    pipeline = RAGPipeline()
    pipeline.build_index(AppConfig().docs_dir)
    return pipeline


def main():
    st.title("📚 RAG Documentation Assistant")
    st.caption("Ask questions about your technical documentation — powered by hybrid search & LLM generation")

    # Sidebar
    with st.sidebar:
        st.header("Settings")
        top_k = st.slider("Documents to retrieve", 1, 10, 5)

        if st.button("🗑️ Clear conversation"):
            st.session_state.messages = []
            pipeline = load_pipeline()
            pipeline.clear_memory()
            st.rerun()

        st.divider()
        st.markdown("### How it works")
        st.markdown(
            "1. **Ingestion** — Documents are chunked and embedded\n"
            "2. **Hybrid Search** — BM25 + dense retrieval\n"
            "3. **Re-ranking** — Cross-encoder scores relevance\n"
            "4. **Generation** — LLM answers with citations"
        )

    # Load pipeline
    pipeline = load_pipeline()

    # Chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            if msg["role"] == "assistant" and "sources" in msg:
                with st.expander("📎 Sources"):
                    for s in msg["sources"]:
                        st.markdown(
                            f"- **{s['source_file']}** (page {s['page']}, "
                            f"score: {s['relevance_score']:.3f})\n"
                            f"  > {s['preview']}"
                        )

    # User input
    if prompt := st.chat_input("Ask a question about your docs..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Searching and generating..."):
                result = pipeline.query(prompt, top_k=top_k)

            st.markdown(result["answer"])

            with st.expander("📎 Sources"):
                for s in result["sources"]:
                    st.markdown(
                        f"- **{s['source_file']}** (page {s['page']}, "
                        f"score: {s['relevance_score']:.3f})\n"
                        f"  > {s['preview']}"
                    )

        st.session_state.messages.append({
            "role": "assistant",
            "content": result["answer"],
            "sources": result["sources"],
        })


if __name__ == "__main__":
    main()
