from pathlib import Path

import pytest

from src.document_processor import load_knowledge_base_documents, load_markdown_documents


def test_load_markdown_documents_preserves_metadata(tmp_path: Path) -> None:
    file_path = tmp_path / "profile.md"
    file_path.write_text("# Profile\n\nSupply chain operations context.", encoding="utf-8")

    documents = load_markdown_documents(tmp_path, knowledge_base="primary")

    assert len(documents) == 1
    assert "Supply chain operations" in documents[0].content
    assert documents[0].metadata["source_name"] == "profile.md"
    assert documents[0].metadata["knowledge_base"] == "primary"
    assert documents[0].metadata["source"].endswith("profile.md")


def test_load_markdown_documents_requires_markdown_files(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="No markdown files"):
        load_markdown_documents(tmp_path)


def test_load_knowledge_base_documents_loads_primary_and_secondary(tmp_path: Path) -> None:
    primary = tmp_path / "primary"
    secondary = tmp_path / "secondary"
    primary.mkdir()
    secondary.mkdir()
    (primary / "brand_voice.md").write_text("Practical and grounded.", encoding="utf-8")
    (secondary / "use_cases.md").write_text("Forecasting and planning.", encoding="utf-8")

    documents = load_knowledge_base_documents(tmp_path)

    assert {doc.metadata["knowledge_base"] for doc in documents} == {"primary", "secondary"}
    assert {doc.metadata["source_name"] for doc in documents} == {"brand_voice.md", "use_cases.md"}
