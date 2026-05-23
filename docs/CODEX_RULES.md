# Codex Rules

## Expected Agent Workflow

Codex should work comprehensively from:

- `AGENTS.md`
- `PROJECT_REQUIREMENTS.md`
- `docs/CODEX_RULES.md`

Codex should not expect task-by-task implementation prompts from the user.

For each development stage, Codex should:

1. State which stage it is starting.
2. Briefly explain what files it will change.
3. Implement the stage.
4. Summarize what changed.
5. Tell the user what to run next, such as `pytest` or `streamlit run src/ui_app.py`.
6. Ask for feedback before expanding scope or changing architecture.

Codex should build the tool incrementally but independently, following the required MVP sequence.


_____

Always ask the user before implementing the change which is out of the project scope.

## Documentation Rules

When adding functionality, update README.
In case of project scope changes, update AGENTS.md and PROJECT_REQUIREMENTS.md accordingly. Always ask the user's permission to updated these files.

---

## Security Rules

Never expose or print API keys.

Never commit `.env`.

Never include real secrets in examples.

Use `.env.example` for placeholder variables.

---

## Completion Standard

A Codex task is complete only when:

- Code matches the relevant requirement.
- The implementation is simple enough to explain in a demo.
- Related tests pass or the limitation is documented.
- No secrets are exposed.
- The change does not expand scope unexpectedly.