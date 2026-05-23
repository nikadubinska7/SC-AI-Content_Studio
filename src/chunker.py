"""Text chunking for markdown documents."""

from __future__ import annotations

from dataclasses import dataclass

from src.document_processor import Document


@dataclass(frozen=True)
class TextChunk:
    """A chunk of source text with inherited document metadata."""

    text: str
    metadata: dict[str, str | int]


def _split_long_text(text: str, max_chars: int) -> list[str]:
    words = text.split()
    parts: list[str] = []
    current: list[str] = []
    current_length = 0

    for word in words:
        projected = current_length + len(word) + (1 if current else 0)
        if current and projected > max_chars:
            parts.append(" ".join(current))
            current = [word]
            current_length = len(word)
        else:
            current.append(word)
            current_length = projected

    if current:
        parts.append(" ".join(current))
    return parts


def split_text(text: str, max_chars: int = 1_200, overlap_chars: int = 150) -> list[str]:
    """Split text into paragraph-aware chunks."""

    if max_chars <= 0:
        raise ValueError("max_chars must be greater than zero")
    if overlap_chars < 0:
        raise ValueError("overlap_chars cannot be negative")
    if overlap_chars >= max_chars:
        raise ValueError("overlap_chars must be smaller than max_chars")

    paragraphs = [paragraph.strip() for paragraph in text.split("\n\n") if paragraph.strip()]
    chunks: list[str] = []
    current = ""

    for paragraph in paragraphs:
        paragraph_parts = (
            _split_long_text(paragraph, max_chars) if len(paragraph) > max_chars else [paragraph]
        )
        for part in paragraph_parts:
            candidate = f"{current}\n\n{part}".strip() if current else part
            if current and len(candidate) > max_chars:
                chunks.append(current)
                overlap = current[-overlap_chars:].strip() if overlap_chars else ""
                overlapped = f"{overlap}\n\n{part}".strip() if overlap else part
                current = overlapped if len(overlapped) <= max_chars else part
            else:
                current = candidate

    if current:
        chunks.append(current)

    return chunks


def chunk_document(
    document: Document,
    max_chars: int = 1_200,
    overlap_chars: int = 150,
) -> list[TextChunk]:
    """Split a document into chunks while preserving source metadata."""

    text_chunks = split_text(document.content, max_chars=max_chars, overlap_chars=overlap_chars)
    source_name = document.metadata.get("source_name", "document")
    chunks: list[TextChunk] = []

    for index, text in enumerate(text_chunks):
        metadata: dict[str, str | int] = {
            **document.metadata,
            "chunk_index": index,
            "chunk_id": f"{source_name}:{index}",
        }
        chunks.append(TextChunk(text=text, metadata=metadata))

    return chunks


def chunk_documents(
    documents: list[Document],
    max_chars: int = 1_200,
    overlap_chars: int = 150,
) -> list[TextChunk]:
    """Split multiple documents into chunks."""

    chunks: list[TextChunk] = []
    for document in documents:
        chunks.extend(chunk_document(document, max_chars=max_chars, overlap_chars=overlap_chars))
    return chunks
