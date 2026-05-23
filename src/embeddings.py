"""OpenAI embedding helpers."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_EMBEDDING_MODEL = "text-embedding-3-small"


@dataclass
class OpenAIEmbeddingClient:
    """Create embeddings with the OpenAI API."""

    model: str = DEFAULT_EMBEDDING_MODEL

    def __post_init__(self) -> None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Add it to your local .env file before generating embeddings."
            )
        self._client = OpenAI(api_key=api_key)

    def embed_texts(self, texts: list[str]) -> list[list[float]]:
        """Return embedding vectors for a batch of texts."""

        cleaned_texts = [text.strip() for text in texts if text.strip()]
        if not cleaned_texts:
            raise ValueError("No non-empty texts were provided for embedding.")

        response = self._client.embeddings.create(model=self.model, input=cleaned_texts)
        return [item.embedding for item in response.data]

    def embed_query(self, query: str) -> list[float]:
        """Return one embedding vector for a retrieval query."""

        if not query.strip():
            raise ValueError("Query cannot be empty.")
        return self.embed_texts([query])[0]


def create_embedding_client(model: str = DEFAULT_EMBEDDING_MODEL) -> OpenAIEmbeddingClient:
    """Create the configured embedding client."""

    return OpenAIEmbeddingClient(model=model)
