# Project Summary

Project name: SupplyChain AI Content Studio

Problem we are solving:
Consultants need consistent, specific, and credible LinkedIn content, but generic AI-generated posts often sound repetitive and disconnected from real experience. This project creates a personal brand content tool that uses my own profile, project examples, past LinkedIn posts, and AI-in-supply-chain research to generate weekly content ideas, briefs, and LinkedIn drafts in my own voice.

Target user:
An AI automation and supply chain consultant who wants to publish one high-quality LinkedIn post per week.


MVP:
A Python-based RAG content generation tool that:
- Ingests markdown files from primary and secondary knowledge bases.
- Splits documents into chunks.
- Creates embeddings.
- Stores chunks in a local vector database.
- Retrieves relevant context for a content request.
- Generates LinkedIn content ideas, briefs, and draft posts.
- The output reflects my supply chain, operations, and AI automation background.
- Produces a side-by-side uniqueness comparison against generic ChatGPT output.
- Shows which knowledge base sources were used for the generated output.

Out of scope for MVP:
- Automated LinkedIn publishing.
- Live market monitoring.
- Multi-user login.
- Production deployment.
- Advanced dashboard.