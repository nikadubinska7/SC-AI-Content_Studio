"""Local ChromaDB vector store wrapper."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import chromadb

from src.chunker import TextChunk
from src.retriever import VectorSearchResult


DEFAULT_CHROMA_PATH = "data/chroma"
DEFAULT_COLLECTION_NAME = "supplychain_content_chunks"


def _clean_metadata(metadata: dict[str, Any]) -> dict[str, str | int | float | bool]:
    cleaned: dict[str, str | int | float | bool] = {}
    for key, value in metadata.items():
        if isinstance(value, str | int | float | bool):
            cleaned[key] = value
        elif value is not None:
            cleaned[key] = str(value)
    return cleaned


class ChromaVectorStore:
    """Persist and query text chunks with ChromaDB."""

    def __init__(
        self,
        persist_path: str | Path = DEFAULT_CHROMA_PATH,
        collection_name: str = DEFAULT_COLLECTION_NAME,
    ) -> None:
        self.persist_path = Path(persist_path)
        self.collection_name = collection_name
        self.persist_path.mkdir(parents=True, exist_ok=True)
        self._client = chromadb.PersistentClient(path=str(self.persist_path))
        self._collection = self._client.get_or_create_collection(name=self.collection_name)

    def reset(self) -> None:
        """Delete and recreate the collection."""

        try:
            self._client.delete_collection(name=self.collection_name)
        except ValueError:
            pass
        self._collection = self._client.get_or_create_collection(name=self.collection_name)

    def add_chunks(self, chunks: list[TextChunk], embeddings: list[list[float]]) -> None:
        """Store chunks and their embedding vectors."""

        if not chunks:
            raise ValueError("No chunks were provided for vector storage.")
        if len(chunks) != len(embeddings):
            raise ValueError("The number of chunks must match the number of embeddings.")

        ids = [str(chunk.metadata["chunk_id"]) for chunk in chunks]
        documents = [chunk.text for chunk in chunks]
        metadatas = [_clean_metadata(chunk.metadata) for chunk in chunks]

        self._collection.upsert(
            ids=ids,
            documents=documents,
            metadatas=metadatas,
            embeddings=embeddings,
        )

    def query_by_embedding(self, query_embedding: list[float], top_k: int = 5) -> list[VectorSearchResult]:
        """Return the nearest chunks for a query embedding."""

        if top_k <= 0:
            raise ValueError("top_k must be greater than zero.")

        result = self._collection.query(query_embeddings=[query_embedding], n_results=top_k)
        ids = result.get("ids", [[]])[0]
        documents = result.get("documents", [[]])[0]
        metadatas = result.get("metadatas", [[]])[0]
        distances = result.get("distances", [[]])[0] if result.get("distances") else []

        search_results: list[VectorSearchResult] = []
        for index, chunk_id in enumerate(ids):
            search_results.append(
                VectorSearchResult(
                    id=chunk_id,
                    text=documents[index],
                    metadata=metadatas[index] or {},
                    distance=distances[index] if index < len(distances) else None,
                )
            )
        return search_results

    def count(self) -> int:
        """Return the number of stored chunks."""

        return int(self._collection.count())
