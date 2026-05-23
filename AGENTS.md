# AGENTS.md

## Project Overview

Project name: SupplyChain AI Content Studio

This project is a Python and Streamlit application that helps generate LinkedIn content ideas, briefs, and draft posts using:

- A primary personal brand knowledge base
- A secondary AI-in-supply-chain research knowledge base
- Markdown document ingestion
- Text chunking
- Embeddings
- Local vector search
- Prompt templates
- LLM-generated content drafts
- Human review before publishing

The user is a supply chain operations professional developing AI consulting and integration expertise. The tool should help demonstrate growing expertise, analytical thinking, applied AI learning, and prototype-building capability.

The app should not present the user as an established AI implementation consultant with active clients.

---

## Core Product Goal

Build a simple Streamlit app where the user can:

1. Enter a topic or content request.
2. Choose output type:
   - LinkedIn content ideas
   - Content brief
   - Draft LinkedIn post
3. Retrieve relevant context from the knowledge base.
4. Generate output using the retrieved context and brand voice rules.
5. Review the source files or chunks used.
6. Copy the result for manual editing before posting.

---

## Required MVP Architecture

Use this structure:

```text
src/
├── document_processor.py
├── chunker.py
├── embeddings.py
├── vector_store.py
├── retriever.py
├── knowledge_base.py
├── prompt_templates.py
├── llm_integration.py
├── content_pipeline.py
├── ui_app.py
└── main.py
```

Expected responsibilities:

- `document_processor.py`: load markdown files and metadata.
- `chunker.py`: split documents into chunks.
- `embeddings.py`: create embeddings using the configured provider.
- `vector_store.py`: create, persist, and query local ChromaDB vector store.
- `retriever.py`: retrieve relevant chunks for a user request.
- `knowledge_base.py`: coordinate loading and indexing of primary and secondary knowledge base files.
- `prompt_templates.py`: store reusable prompt templates.
- `llm_integration.py`: call the LLM API.
- `content_pipeline.py`: orchestrate retrieve → prompt → generate.
- `ui_app.py`: Streamlit interface.
- `main.py`: optional helper entry point for indexing or smoke testing.

---

## Technical Stack

Use:

- Python 3.11
- Streamlit
- OpenAI API
- ChromaDB
- python-dotenv
- markdown or standard file parsing
- pytest

Do not add heavy frameworks unless required.

---

## Environment Variables

Use `.env` for secrets.

Expected variable:

```text
OPENAI_API_KEY=
```

Never hardcode secrets.

Never commit `.env`.

Use `.env.example` for placeholder variable names only.

---

## Coding Rules

- Keep code simple and readable.
- Prefer small functions with clear names.
- Use type hints where practical.
- Use docstrings for public functions.
- Add clear error messages.
- Preserve source metadata during ingestion, chunking, storage, and retrieval.
- Keep prompt templates separate from pipeline logic.
- Do not mix UI logic with retrieval or LLM logic.
- Avoid unnecessary abstraction.
- Do not silently swallow exceptions.

---

## RAG Scope

This project uses lightweight local RAG.

Required:

- Load markdown files.
- Split into chunks.
- Embed chunks.
- Store in local ChromaDB.
- Retrieve relevant chunks.
- Generate content using retrieved context.

Not required:

- Production RAG deployment.
- Advanced evaluation framework.
- Multi-user auth.
- Cloud vector database.
- Automated LinkedIn publishing.
- Live web monitoring.

---

## Voice and Positioning Rules

Generated content must follow the primary knowledge base, especially:

- `knowledge_base/primary/profile.md`
- `knowledge_base/primary/brand_voice.md`
- `knowledge_base/primary/past_posts.md`
- `knowledge_base/primary/project_examples.md`

Important:

- Do not write as if the user is already an established AI implementation consultant.
- Do not use “I help companies...” positioning.
- Do not claim client results.
- Do not overstate expertise.
- Frame content as practical analysis, exploration, prototype-building, applied learning, and supply-chain-informed AI thinking.
- Keep the tone practical, analytical, human, and grounded.
- Avoid AI hype.

---

## Testing Expectations

At minimum, maintain tests for:

- Markdown document loading
- Chunking logic
- Retrieval behavior

Run tests with:

```bash
pytest
```

---

## Streamlit App

Run the app with:

```bash
streamlit run src/ui_app.py
```

The UI should include:

- Text input or text area for content request
- Output type selector
- Generate button
- Generated result display
- Retrieved source/context display
- Human review reminder

---

## Human Review Requirement

Generated LinkedIn posts are drafts only.

The app should remind the user to review, edit, and approve the content before posting.

---

## Change Control

Do not expand scope without explicit user approval.

If a requirement changes, update:

- `PROJECT_REQUIREMENTS.md`
- relevant Trello card
- prompt tracking log, if AI-generated code was involved
- change log, if the decision affects MVP scope, architecture, or deliverables

Scope changes that require approval:

- Replacing Streamlit with another UI framework
- Replacing ChromaDB with another vector store
- Adding automated LinkedIn publishing
- Adding live web monitoring
- Adding authentication
- Adding cloud deployment
- Adding advanced analytics
- Changing the user positioning or brand voice rules
- Removing required course deliverables

---

## Development Sequence

Build the project in small, reviewable steps.

Recommended order:

1. Implement markdown document loading.
2. Implement text chunking.
3. Implement embeddings.
4. Implement local ChromaDB vector storage.
5. Implement retrieval.
6. Implement prompt templates.
7. Implement LLM integration.
8. Implement the content generation pipeline.
9. Implement the Streamlit UI.
10. Add tests and polish documentation.

Do not start with the UI before the core pipeline exists.

Do not build advanced features before the MVP works end to end.

---

## Definition of Done for Codex Tasks

A Codex task is complete only when:

- The relevant requirement is implemented.
- The code is readable and modular.
- The code follows file responsibility rules.
- Secrets are not exposed.
- Source metadata is preserved where relevant.
- Errors are handled clearly.
- Tests are added or updated for core logic.
- The user can explain the change in the final demo.

---

## Final Demo Expectations

The final project demo should show:

1. Knowledge base markdown files.
2. Document ingestion.
3. Chunking and vector indexing.
4. Retrieved source context.
5. Generated LinkedIn content idea, brief, or post.
6. Streamlit UI workflow.
7. Human review step.
8. Explanation of how the output differs from generic ChatGPT content.

---

## Important Project Boundaries

This is a student project and prototype.

The code should prioritize:

- Clarity over complexity
- Working MVP over advanced architecture
- Explainability over hidden automation
- Human review over full automation
- Practical AI-in-supply-chain use cases over generic AI content

Do not optimize prematurely.
```