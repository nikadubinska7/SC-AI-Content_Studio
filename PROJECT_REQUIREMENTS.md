# Project Requirements

## 1. Project Summary

**Project name:** SupplyChain AI Content Studio

**Problem we are solving:**  
Consultants need consistent, credible, and specific LinkedIn content, but generic AI-generated posts often sound repetitive and disconnected from real operational experience. This project creates a personal brand content tool that uses my LinkedIn profile, past content, project examples, and AI-in-supply-chain research to generate weekly LinkedIn content ideas, briefs, and draft posts in my own voice.

**Target user:**  
An AI automation and supply chain consultant who wants to publish one high-quality LinkedIn post per week.

**Primary content channel:**  
LinkedIn.

**Success criteria:**
- The app ingests markdown files from both primary and secondary knowledge bases.
- The app chunks documents and stores them in a local vector database.
- The app retrieves relevant knowledge base context for a content request.
- The app generates weekly LinkedIn content ideas, a content brief, and a draft post.
- The output reflects my supply chain, operations, business process automation, and AI automation background.
- The repository includes README, requirements.txt, AGENTS.md, Codex rules, and this PROJECT_REQUIREMENTS.md file.

---

## 2. Scope

### Must Have

- [ ] Project structure follows the required course layout.
- [ ] Primary knowledge base contains markdown files about my profile, brand voice, services, past posts, and project examples.
- [ ] Secondary knowledge base contains markdown files about AI in supply chain trends, client pain points, competitor positioning, and use cases.
- [ ] Python app can ingest markdown files from both knowledge bases.
- [ ] Python app can split documents into chunks.
- [ ] Python app can create embeddings for chunks.
- [ ] Python app can store and query chunks using a local vector store.
- [ ] Python app can retrieve relevant context for a content request.
- [ ] Python app can generate LinkedIn content ideas, briefs, and draft posts.
- [ ] Prompt templates are reusable and separated from pipeline logic.
- [ ] API keys are loaded from `.env` and never committed.
- [ ] Basic tests exist for document processing, chunking, and retrieval.
- [ ] README explains setup, usage, and demo flow.
- [ ] Simple Streamlit UI allows the user to enter a content request and choose output type: ideas, brief, or post.


### Should Have

- [ ] Generated output includes source references or document names used for context.
- [ ] UI displays retrieved source documents used for generation.
- [ ] Example output is saved under `data/outputs/`.
- [ ] Human review checklist is included with generated content.
- [ ] Codex usage rules are documented clearly in `AGENTS.md` and `docs/CODEX_RULES.md`.

### Could Have

- [ ] Add scoring for brand alignment.
- [ ] Add multiple post styles.
- [ ] Add export to markdown.
- [ ] Add automatic content calendar suggestions.

### Out of Scope

- Automated LinkedIn publishing.
- Live web monitoring.
- Multi-user login.
- Production deployment.
- Advanced analytics dashboard.
- Complex enterprise RAG architecture.
- Paid database hosting.
- Fully automated content approval without human review.

---

## 3. Functional Requirements

| ID | Requirement | Acceptance Criteria | Trello Card |
|----|-------------|---------------------|-------------|
| FR-001 | The app can ingest markdown files from both knowledge bases. | Given valid markdown files in `knowledge_base/primary` and `knowledge_base/secondary`, when the ingestion script runs, then document content and metadata are loaded successfully. | Implement Markdown Document Processor |
| FR-002 | The app can split documents into chunks. | Given loaded markdown content, when chunking runs, then text is split into usable chunks with source metadata preserved. | Implement Text Chunking Logic |
| FR-003 | The app can create embeddings for chunks. | Given text chunks, when embedding generation runs, then each chunk receives an embedding vector. | Implement Embeddings Integration |
| FR-004 | The app can store chunks in a local vector store. | Given embedded chunks, when indexing runs, then chunks are stored in ChromaDB or equivalent local vector storage. | Implement Local Vector Store with ChromaDB |
| FR-005 | The app can retrieve relevant context. | Given a user content request, when retrieval runs, then the most relevant chunks are returned with source metadata. | Implement Retriever for Relevant Context |
| FR-006 | The app can generate LinkedIn content ideas. | Given retrieved context, when the user requests ideas, then the app generates several specific LinkedIn content ideas. | Build Content Generation Pipeline |
| FR-007 | The app can generate a content brief. | Given a selected idea and retrieved context, when brief generation runs, then the app outputs objective, audience, key message, supporting points, and suggested structure. | Build Content Generation Pipeline |
| FR-008 | The app can generate a LinkedIn draft post. | Given a brief and retrieved context, when post generation runs, then the app outputs a LinkedIn-ready draft in the target personal brand voice. | Build Content Generation Pipeline |
| FR-009 | Prompt templates are reusable. | Prompt templates are stored separately from execution logic and can be modified without rewriting the pipeline. | Create Prompt Templates for LinkedIn Content |
| FR-010 | The app has a simple Streamlit UI. | Given the user opens the app in a browser, when they enter a topic/request and choose an output type, then the app generates LinkedIn ideas, a brief, or a draft post using retrieved knowledge base context. | Create Simple Streamlit UI |
| FR-011 | The UI displays source context used for generation. | Given generated content is produced, when the result is shown, then the UI displays the source file names or document chunks used by the retriever. | Create Simple Streamlit UI |
| FR-012 | The app protects secrets. | API keys are read from `.env`; `.env` is ignored by Git; `.env.example` documents required variables. | Create Conda Environment and Dependency Files |
| FR-013 | The project includes basic tests. | Tests cover document processing, chunking, and retrieval logic. | Write Basic Tests for Processor, Chunker, and Retriever |

---

## 4. Non-Functional Requirements

**Reliability:**  
The app should fail clearly when knowledge base files are missing, API keys are unavailable, or the vector store has not been built.

**Privacy and API-key handling:**  
API keys must be stored in `.env`, not hardcoded. `.env` must not be committed.

**Maintainability:**  
The code should be modular. Each source file should have one clear responsibility.

**Usability:**  
The first version uses a simple Streamlit UI. The user should be able to enter a content request, choose an output type, generate content, review retrieved sources, and copy the result for manual editing before posting.

**Explainability:**  
Generated content should show which knowledge base files or chunks influenced the output where possible.

**Human review:**  
Generated posts are drafts only. The user reviews and edits before publishing.

---

## 5. AI Coding-Agent Rules

**AI coding agent used:**  
Codex / VSCode coding agent.

**What the agent is allowed to do:**
- Implement Python modules based on existing requirements.
- Suggest refactoring while preserving project scope.
- Write tests for existing functionality.
- Improve README and documentation.
- Help debug errors.

**What the agent is not allowed to do:**
- Commit secrets or API keys.
- Remove required project files.
- Expand MVP scope without approval.
- Replace the project architecture without explanation.
- Add unnecessary frameworks before the CLI MVP works.
- Skip tests for core modules.
- Generate final LinkedIn posts without keeping human review in the workflow.

**Human review process:**
- Review generated code before accepting.
- Run tests after significant code changes.
- Check that generated code follows file responsibilities.
- Log meaningful prompts in the prompt tracking table.
- Update the change log if scope changes.

**Secrets and private data protection:**
- `.env` is ignored by Git.
- `.env.example` documents required variables only.
- Personal LinkedIn/profile content is used only as local project knowledge base material.