"""Knowledge base loading, chunking, and indexing orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from src.chunker import TextChunk, chunk_documents
from src.document_processor import Document, load_knowledge_base_documents
from src.embeddings import OpenAIEmbeddingClient, create_embedding_client
from src.vector_store import ChromaVectorStore


DEFAULT_KNOWLEDGE_BASE_PATH = "knowledge_base"
DEFAULT_CHUNK_SIZE = 1_200
DEFAULT_CHUNK_OVERLAP = 150


@dataclass(frozen=True)
class KnowledgeBaseBuildResult:
    """Summary of a knowledge base indexing run."""

    document_count: int
    chunk_count: int


def load_documents(base_path: str | Path = DEFAULT_KNOWLEDGE_BASE_PATH) -> list[Document]:
    """Load all primary and secondary knowledge base documents."""

    return load_knowledge_base_documents(base_path)


def load_chunks(
    base_path: str | Path = DEFAULT_KNOWLEDGE_BASE_PATH,
    max_chars: int = DEFAULT_CHUNK_SIZE,
    overlap_chars: int = DEFAULT_CHUNK_OVERLAP,
) -> list[TextChunk]:
    """Load and chunk the complete knowledge base."""

    documents = load_documents(base_path)
    return chunk_documents(documents, max_chars=max_chars, overlap_chars=overlap_chars)


def _embed_in_batches(
    chunks: list[TextChunk],
    embedding_client: OpenAIEmbeddingClient,
    batch_size: int,
) -> list[list[float]]:
    embeddings: list[list[float]] = []
    for start in range(0, len(chunks), batch_size):
        batch = chunks[start : start + batch_size]
        embeddings.extend(embedding_client.embed_texts([chunk.text for chunk in batch]))
    return embeddings


def rebuild_vector_index(
    base_path: str | Path = DEFAULT_KNOWLEDGE_BASE_PATH,
    vector_store: ChromaVectorStore | None = None,
    embedding_client: OpenAIEmbeddingClient | None = None,
    batch_size: int = 64,
) -> KnowledgeBaseBuildResult:
    """Rebuild the local ChromaDB index from markdown knowledge base files."""

    if batch_size <= 0:
        raise ValueError("batch_size must be greater than zero.")

    documents = load_documents(base_path)
    chunks = chunk_documents(
        documents,
        max_chars=DEFAULT_CHUNK_SIZE,
        overlap_chars=DEFAULT_CHUNK_OVERLAP,
    )
    if not chunks:
        raise ValueError("No chunks were created from the knowledge base.")

    store = vector_store or ChromaVectorStore()
    client = embedding_client or create_embedding_client()

    embeddings = _embed_in_batches(chunks, client, batch_size=batch_size)
    store.reset()
    store.add_chunks(chunks, embeddings)

    return KnowledgeBaseBuildResult(document_count=len(documents), chunk_count=len(chunks))
