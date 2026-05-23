# SupplyChain AI Content Studio

A Python and Streamlit application that generates LinkedIn content ideas, briefs, and draft posts using a personal brand knowledge base and AI-in-supply-chain research.

This project is built for Project 2: AI Content Creator.

## Project Purpose

Generic AI-generated LinkedIn posts often sound repetitive and disconnected from real experience.

This tool uses:

- A primary personal brand knowledge base
- A secondary AI-in-supply-chain research knowledge base
- Markdown ingestion
- Document chunking
- Embeddings
- Local vector search
- Prompt templates
- LLM-generated content drafts
- Human review before publishing

The goal is to support weekly LinkedIn content creation around practical AI use in business, supply chain operations, and business process automation.

## Positioning

The content should reflect the perspective of a supply chain operations professional developing AI consulting and integration expertise.

The generated posts should show:

- Practical business thinking
- Supply chain and operations context
- Awareness of current AI trends
- Analytical reasoning
- Applied learning
- Prototype-building capability

The tool should not overclaim expertise or present the user as an established AI implementation consultant.

## Project Structure

```text
supplychain-ai-content-studio/
├── AGENTS.md
├── PROJECT_REQUIREMENTS.md
├── README.md
├── requirements.txt
├── .env.example
├── data/
│   └── outputs/
├── docs/
│   ├── CODEX_RULES.md
│   └── uniqueness_evidence.md
├── config/
│   └── vscode_agent.json
├── knowledge_base/
│   ├── primary/
│   └── secondary/
├── src/
│   ├── document_processor.py
│   ├── chunker.py
│   ├── embeddings.py
│   ├── vector_store.py
│   ├── retriever.py
│   ├── knowledge_base.py
│   ├── prompt_templates.py
│   ├── llm_integration.py
│   ├── content_pipeline.py
│   ├── ui_app.py
│   └── main.py
└── tests/
```

## Knowledge Bases

### Primary Knowledge Base

Located in:

```text
knowledge_base/primary/
```

Contains personal brand and positioning context:

- `profile.md`
- `brand_voice.md`
- `services.md`
- `past_posts.md`
- `project_examples.md`

### Secondary Knowledge Base

Located in:

```text
knowledge_base/secondary/
```

Contains AI and supply-chain research context:

- `ai_supply_chain_trends.md`
- `client_pain_points.md`
- `competitor_positioning.md`
- `use_cases.md`

## MVP Features

The MVP should:

- Ingest markdown files from both knowledge bases
- Split documents into chunks
- Create embeddings for chunks
- Store chunks in a local ChromaDB vector store
- Retrieve relevant context for a user request
- Generate LinkedIn content ideas, briefs, or draft posts
- Show retrieved source context
- Provide a human review reminder
- Run through a simple Streamlit UI

## Out of Scope

The MVP does not include:

- Automated LinkedIn publishing
- Live web monitoring
- Multi-user login
- Production deployment
- Advanced analytics dashboard
- Cloud vector database
- Fully automated content approval

## Setup

### 1. Create and activate Conda environment

```bash
conda create -n supplychain-ai-content python=3.11 -y
conda activate supplychain-ai-content
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create local `.env`

Copy `.env.example` into `.env`:

```bash
cp .env.example .env
```

Then add your real OpenAI API key:

```env
OPENAI_API_KEY=your_real_key_here
```

Do not commit `.env`.

## Run Tests

```bash
pytest
```

## Run the App

```bash
streamlit run src/ui_app.py
```

## Expected User Flow

1. Open the Streamlit app.
2. Enter a content topic or request.
3. Choose output type:
   - LinkedIn content ideas
   - Content brief
   - Draft LinkedIn post
4. Generate content.
5. Review retrieved sources.
6. Edit manually before publishing on LinkedIn.

## Demo Flow

The final demo should show:

1. Knowledge base markdown files.
2. Document ingestion.
3. Chunking and vector search.
4. Retrieved source context.
5. Generated LinkedIn output.
6. Streamlit UI.
7. Human review step.
8. Difference between generic ChatGPT output and tool-generated output.

## Human Review Note

Generated posts are drafts only.

The user must review and edit the content before publishing. The system is intended to support thinking and drafting, not to fully automate personal brand content.