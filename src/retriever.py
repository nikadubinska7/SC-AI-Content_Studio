"""Retrieve relevant knowledge base chunks for a content request."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

class EmbeddingProvider(Protocol):
    """Protocol for query embedding providers."""

    def embed_query(self, query: str) -> list[float]:
        """Create an embedding for a query."""


class VectorStore(Protocol):
    """Protocol for vector stores used by the retriever."""

    def query_by_embedding(self, query_embedding: list[float], top_k: int = 5) -> list[VectorSearchResult]:
        """Return relevant chunks for an embedding."""


@dataclass(frozen=True)
class VectorSearchResult:
    """A generic vector search result returned by a store."""

    id: str
    text: str
    metadata: dict[str, object]
    distance: float | None = None


@dataclass(frozen=True)
class RetrievedChunk:
    """A retrieved chunk prepared for prompt and UI display."""

    text: str
    source_name: str
    knowledge_base: str
    chunk_id: str
    distance: float | None = None


class Retriever:
    """Retrieve relevant chunks using an embedding provider and vector store."""

    def __init__(self, embedding_provider: EmbeddingProvider, vector_store: VectorStore) -> None:
        self.embedding_provider = embedding_provider
        self.vector_store = vector_store

    def retrieve(self, query: str, top_k: int = 5) -> list[RetrievedChunk]:
        """Retrieve the top matching chunks for a user query."""

        if not query.strip():
            raise ValueError("Content request cannot be empty.")
        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        query_embedding = self.embedding_provider.embed_query(query)
        results = self.vector_store.query_by_embedding(query_embedding, top_k=top_k)

        return [
            RetrievedChunk(
                text=result.text,
                source_name=str(result.metadata.get("source_name", "unknown")),
                knowledge_base=str(result.metadata.get("knowledge_base", "unknown")),
                chunk_id=str(result.metadata.get("chunk_id", result.id)),
                distance=result.distance,
            )
            for result in results
        ]


def format_retrieved_context(chunks: list[RetrievedChunk]) -> str:
    """Format retrieved chunks for prompt context."""

    if not chunks:
        return "No relevant source context was retrieved."

    formatted_chunks = []
    for index, chunk in enumerate(chunks, start=1):
        formatted_chunks.append(
            "\n".join(
                [
                    f"[Source {index}: {chunk.source_name} | {chunk.knowledge_base} | {chunk.chunk_id}]",
                    chunk.text,
                ]
            )
        )
    return "\n\n".join(formatted_chunks)
