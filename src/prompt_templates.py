"""Reusable prompt templates for LinkedIn content generation."""

from __future__ import annotations

from enum import StrEnum


class OutputType(StrEnum):
    """Supported content generation outputs."""

    IDEAS = "LinkedIn content ideas"
    BRIEF = "Content brief"
    POST = "Draft LinkedIn post"


SYSTEM_PROMPT = """You are a careful LinkedIn content drafting assistant.

Use the provided knowledge-base context to support practical, grounded content about AI, supply chain operations, automation, and applied learning.

Positioning rules:
- Do not present the author as an established AI implementation consultant with active clients.
- Do not use "I help companies..." positioning.
- Do not claim client results, revenue impact, or implementation outcomes that are not in the source context.
- Frame the author as a supply chain operations professional developing AI consulting and integration expertise.
- Emphasize practical analysis, exploration, prototype-building, applied learning, and supply-chain-informed AI thinking.
- Keep the tone practical, analytical, human, and grounded.
- Avoid AI hype, vague transformation language, and exaggerated certainty.

Every output is a draft for human review before publishing."""


IDEAS_TEMPLATE = """Content request:
{request}

Retrieved knowledge-base context:
{context}

Create 5 LinkedIn content ideas.

For each idea include:
- Working title
- Main angle
- Why it is relevant to supply chain or operations
- Source connection from the retrieved context
- A short note on how to keep the post grounded and non-hype"""


BRIEF_TEMPLATE = """Content request:
{request}

Retrieved knowledge-base context:
{context}

Create a content brief for one LinkedIn post.

Include:
- Draft topic
- Objective
- Target reader
- Key message
- Supporting points
- Practical supply chain or operations connection
- Suggested structure
- Sources to review before writing
- Human review checklist"""


POST_TEMPLATE = """Content request:
{request}

Retrieved knowledge-base context:
{context}

Write a draft LinkedIn post.

Requirements:
- Use a practical first-person perspective only when supported by the source context.
- Avoid "I help companies..." and avoid claiming client work or implementation outcomes.
- Make the post specific to supply chain operations, AI automation, or prototype-building.
- Keep it concise enough for LinkedIn.
- End with a thoughtful question or reflection, not a sales pitch.
- Add a short "Human review before posting" checklist after the draft."""


def build_user_prompt(output_type: OutputType | str, request: str, context: str) -> str:
    """Build the user prompt for a supported output type."""

    normalized = OutputType(output_type)
    template_by_type = {
        OutputType.IDEAS: IDEAS_TEMPLATE,
        OutputType.BRIEF: BRIEF_TEMPLATE,
        OutputType.POST: POST_TEMPLATE,
    }
    return template_by_type[normalized].format(request=request.strip(), context=context.strip())
