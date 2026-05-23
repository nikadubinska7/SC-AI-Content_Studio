import pytest

from src.retriever import Retriever, VectorSearchResult, format_retrieved_context


class FakeEmbeddingProvider:
    def embed_query(self, query: str) -> list[float]:
        assert "forecasting" in query
        return [0.1, 0.2, 0.3]


class FakeVectorStore:
    def query_by_embedding(self, query_embedding: list[float], top_k: int = 5) -> list[VectorSearchResult]:
        assert query_embedding == [0.1, 0.2, 0.3]
        assert top_k == 2
        return [
            VectorSearchResult(
                id="use_cases.md:0",
                text="AI can support demand forecasting workflows.",
                metadata={
                    "source_name": "use_cases.md",
                    "knowledge_base": "secondary",
                    "chunk_id": "use_cases.md:0",
                },
                distance=0.12,
            )
        ]


def test_retriever_returns_chunks_with_metadata() -> None:
    retriever = Retriever(FakeEmbeddingProvider(), FakeVectorStore())

    chunks = retriever.retrieve("forecasting process improvement", top_k=2)

    assert len(chunks) == 1
    assert chunks[0].source_name == "use_cases.md"
    assert chunks[0].knowledge_base == "secondary"
    assert chunks[0].chunk_id == "use_cases.md:0"
    assert "forecasting" in chunks[0].text


def test_retriever_rejects_empty_query() -> None:
    retriever = Retriever(FakeEmbeddingProvider(), FakeVectorStore())

    with pytest.raises(ValueError, match="cannot be empty"):
        retriever.retrieve(" ")


def test_format_retrieved_context_includes_source_labels() -> None:
    retriever = Retriever(FakeEmbeddingProvider(), FakeVectorStore())
    chunks = retriever.retrieve("forecasting process improvement", top_k=2)

    context = format_retrieved_context(chunks)

    assert "[Source 1: use_cases.md | secondary | use_cases.md:0]" in context
    assert "demand forecasting" in context
