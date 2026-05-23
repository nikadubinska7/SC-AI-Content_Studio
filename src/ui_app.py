"""Streamlit UI for SupplyChain AI Content Studio."""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st


PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.content_pipeline import ContentPipeline
from src.embeddings import create_embedding_client
from src.knowledge_base import rebuild_vector_index
from src.llm_integration import create_content_client
from src.prompt_templates import OutputType
from src.retriever import Retriever
from src.vector_store import ChromaVectorStore


@st.cache_resource
def get_vector_store() -> ChromaVectorStore:
    """Return the cached local vector store."""

    return ChromaVectorStore()


@st.cache_resource
def get_pipeline() -> ContentPipeline:
    """Return the cached content pipeline."""

    embedding_client = create_embedding_client()
    vector_store = get_vector_store()
    retriever = Retriever(embedding_client, vector_store)
    content_client = create_content_client()
    return ContentPipeline(retriever, content_client)


def render_sources(generated_chunks) -> None:
    """Render retrieved source chunks."""

    if not generated_chunks:
        st.info("No retrieved source context was returned.")
        return

    for index, chunk in enumerate(generated_chunks, start=1):
        label = f"{index}. {chunk.source_name} ({chunk.knowledge_base})"
        with st.expander(label):
            st.caption(f"Chunk: {chunk.chunk_id}")
            if chunk.distance is not None:
                st.caption(f"Distance: {chunk.distance:.4f}")
            st.write(chunk.text)


def main() -> None:
    """Render the Streamlit app."""

    st.set_page_config(page_title="SupplyChain AI Content Studio", layout="wide")

    st.title("SupplyChain AI Content Studio")
    st.caption("Draft LinkedIn ideas, briefs, and posts from local supply chain + AI knowledge base context.")

    with st.sidebar:
        st.header("Knowledge Base")
        try:
            vector_store = get_vector_store()
            st.metric("Indexed chunks", vector_store.count())
        except Exception as exc:
            st.warning(f"Vector store is not ready: {exc}")

        if st.button("Rebuild local index"):
            with st.spinner("Embedding markdown files and rebuilding ChromaDB..."):
                try:
                    result = rebuild_vector_index(vector_store=get_vector_store())
                    get_pipeline.clear()
                    st.success(f"Indexed {result.document_count} documents into {result.chunk_count} chunks.")
                except Exception as exc:
                    st.error(f"Index rebuild failed: {exc}")

        st.divider()
        st.info("Generated content is a draft. Review and edit before publishing.")

    request = st.text_area(
        "Content request",
        placeholder="Example: Create a LinkedIn post about practical AI use cases in demand planning.",
        height=140,
    )
    output_type = st.selectbox(
        "Output type",
        options=[output.value for output in OutputType],
        index=0,
    )
    top_k = st.slider("Retrieved chunks", min_value=2, max_value=8, value=5)

    if st.button("Generate", type="primary"):
        if not request.strip():
            st.error("Enter a content request before generating.")
            return

        with st.spinner("Retrieving context and generating draft content..."):
            try:
                generated = get_pipeline().generate(
                    request=request,
                    output_type=OutputType(output_type),
                    top_k=top_k,
                )
            except Exception as exc:
                st.error(f"Generation failed: {exc}")
                return

        st.subheader(generated.output_type.value)
        st.text_area("Generated draft", generated.content, height=420)

        st.subheader("Retrieved Sources")
        render_sources(generated.retrieved_chunks)

        st.warning(
            "Human review required: check factual accuracy, source fit, tone, positioning, and any claims before posting."
        )


if __name__ == "__main__":
    main()
