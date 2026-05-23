"""Markdown document loading for the knowledge base."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Document:
    """A markdown document with source metadata preserved."""

    content: str
    metadata: dict[str, str]


def load_markdown_file(file_path: str | Path, knowledge_base: str | None = None) -> Document:
    """Load one markdown file and attach source metadata."""

    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"Markdown file not found: {path}")
    if path.suffix.lower() != ".md":
        raise ValueError(f"Expected a markdown file with .md suffix: {path}")

    content = path.read_text(encoding="utf-8").strip()
    if not content:
        raise ValueError(f"Markdown file is empty: {path}")

    metadata = {
        "source": path.as_posix(),
        "source_name": path.name,
        "stem": path.stem,
    }
    if knowledge_base:
        metadata["knowledge_base"] = knowledge_base

    return Document(content=content, metadata=metadata)


def load_markdown_documents(directory: str | Path, knowledge_base: str | None = None) -> list[Document]:
    """Load all markdown files from a directory in deterministic order."""

    path = Path(directory)
    if not path.exists():
        raise FileNotFoundError(f"Knowledge base directory not found: {path}")
    if not path.is_dir():
        raise NotADirectoryError(f"Expected a directory: {path}")

    markdown_files = sorted(path.glob("*.md"))
    if not markdown_files:
        raise ValueError(f"No markdown files found in directory: {path}")

    return [load_markdown_file(file_path, knowledge_base=knowledge_base) for file_path in markdown_files]


def load_knowledge_base_documents(base_path: str | Path = "knowledge_base") -> list[Document]:
    """Load primary and secondary knowledge base markdown documents."""

    root = Path(base_path)
    documents: list[Document] = []
    for knowledge_base in ("primary", "secondary"):
        documents.extend(load_markdown_documents(root / knowledge_base, knowledge_base=knowledge_base))
    return documents
