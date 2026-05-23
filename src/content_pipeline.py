"""Content generation pipeline orchestration."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from src.prompt_templates import OutputType, SYSTEM_PROMPT, build_user_prompt
from src.retriever import RetrievedChunk, Retriever, format_retrieved_context


class ContentGenerator(Protocol):
    """Protocol for LLM content generators."""

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate content from prompts."""


@dataclass(frozen=True)
class GeneratedContent:
    """Generated content and the source context used to create it."""

    output_type: OutputType
    request: str
    content: str
    retrieved_chunks: list[RetrievedChunk]

    @property
    def source_names(self) -> list[str]:
        """Return unique source file names used by retrieval."""

        return sorted({chunk.source_name for chunk in self.retrieved_chunks})


class ContentPipeline:
    """Run retrieve → prompt → generate for LinkedIn content."""

    def __init__(self, retriever: Retriever, content_generator: ContentGenerator) -> None:
        self.retriever = retriever
        self.content_generator = content_generator

    def generate(self, request: str, output_type: OutputType | str, top_k: int = 5) -> GeneratedContent:
        """Generate the requested LinkedIn content output."""

        if not request.strip():
            raise ValueError("Content request cannot be empty.")

        normalized_output_type = OutputType(output_type)
        retrieved_chunks = self.retriever.retrieve(request, top_k=top_k)
        context = format_retrieved_context(retrieved_chunks)
        user_prompt = build_user_prompt(normalized_output_type, request=request, context=context)
        content = self.content_generator.generate(SYSTEM_PROMPT, user_prompt)

        return GeneratedContent(
            output_type=normalized_output_type,
            request=request.strip(),
            content=content,
            retrieved_chunks=retrieved_chunks,
        )
