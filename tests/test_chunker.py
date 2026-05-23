from src.chunker import chunk_document, split_text
from src.document_processor import Document


def test_split_text_keeps_chunks_under_limit() -> None:
    text = "\n\n".join(
        [
            "Supply chain planning needs clear process context.",
            " ".join(["forecasting"] * 80),
            "AI prototypes should stay grounded in operational constraints.",
        ]
    )

    chunks = split_text(text, max_chars=120, overlap_chars=20)

    assert len(chunks) > 1
    assert all(len(chunk) <= 120 for chunk in chunks)


def test_chunk_document_preserves_metadata() -> None:
    document = Document(
        content="First paragraph about operations.\n\nSecond paragraph about AI learning.",
        metadata={"source_name": "profile.md", "knowledge_base": "primary", "source": "profile.md"},
    )

    chunks = chunk_document(document, max_chars=45, overlap_chars=10)

    assert len(chunks) == 2
    assert chunks[0].metadata["source_name"] == "profile.md"
    assert chunks[0].metadata["knowledge_base"] == "primary"
    assert chunks[0].metadata["chunk_index"] == 0
    assert chunks[1].metadata["chunk_id"] == "profile.md:1"


def test_split_text_rejects_invalid_overlap() -> None:
    try:
        split_text("text", max_chars=100, overlap_chars=100)
    except ValueError as exc:
        assert "overlap_chars" in str(exc)
    else:
        raise AssertionError("Expected ValueError for overlap equal to max_chars")
