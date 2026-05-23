"""Command-line helpers for indexing and smoke testing the MVP pipeline."""

from __future__ import annotations

import argparse

from src.embeddings import create_embedding_client
from src.knowledge_base import rebuild_vector_index
from src.llm_integration import create_content_client
from src.prompt_templates import OutputType
from src.retriever import Retriever
from src.vector_store import ChromaVectorStore
from src.content_pipeline import ContentPipeline


def build_pipeline() -> ContentPipeline:
    """Build the default content pipeline from configured services."""

    embedding_client = create_embedding_client()
    vector_store = ChromaVectorStore()
    retriever = Retriever(embedding_client, vector_store)
    content_client = create_content_client()
    return ContentPipeline(retriever, content_client)


def main() -> None:
    """Run indexing or a simple generation smoke test."""

    parser = argparse.ArgumentParser(description="SupplyChain AI Content Studio helper commands")
    parser.add_argument("--rebuild-index", action="store_true", help="Rebuild the local ChromaDB index")
    parser.add_argument("--request", help="Optional content request for a smoke test")
    parser.add_argument(
        "--output-type",
        choices=[output.value for output in OutputType],
        default=OutputType.IDEAS.value,
        help="Output type for smoke-test generation",
    )
    args = parser.parse_args()

    if args.rebuild_index:
        result = rebuild_vector_index()
        print(f"Indexed {result.document_count} documents into {result.chunk_count} chunks.")

    if args.request:
        pipeline = build_pipeline()
        generated = pipeline.generate(args.request, OutputType(args.output_type))
        print(generated.content)
        print("\nSources:")
        for source in generated.source_names:
            print(f"- {source}")

    if not args.rebuild_index and not args.request:
        parser.print_help()


if __name__ == "__main__":
    main()
