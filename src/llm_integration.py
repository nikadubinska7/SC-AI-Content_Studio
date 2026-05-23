"""OpenAI LLM integration for content drafting."""

from __future__ import annotations

import os
from dataclasses import dataclass

from dotenv import load_dotenv
from openai import OpenAI


DEFAULT_GENERATION_MODEL = "gpt-4o-mini"


@dataclass
class OpenAIContentClient:
    """Generate content with the OpenAI API."""

    model: str = DEFAULT_GENERATION_MODEL
    temperature: float = 0.4

    def __post_init__(self) -> None:
        load_dotenv()
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError(
                "OPENAI_API_KEY is missing. Add it to your local .env file before generating content."
            )
        self._client = OpenAI(api_key=api_key)

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        """Generate text from a system prompt and user prompt."""

        if not system_prompt.strip():
            raise ValueError("System prompt cannot be empty.")
        if not user_prompt.strip():
            raise ValueError("User prompt cannot be empty.")

        response = self._client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )
        content = response.choices[0].message.content
        if not content:
            raise ValueError("OpenAI returned an empty response.")
        return content.strip()


def create_content_client(model: str = DEFAULT_GENERATION_MODEL) -> OpenAIContentClient:
    """Create the configured content generation client."""

    return OpenAIContentClient(model=model)
