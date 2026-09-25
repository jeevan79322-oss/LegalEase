# Phase 3: Project Design

## Architecture

```text
User
  |
  v
Streamlit frontend (app.py) ---- HTTP/JSON ----> FastAPI (main.py, routes.py)
                                                    |
                           +------------------------+-------------------+
                           |                                            |
                           v                                            v
                 Gemini generator                          TXT/DOCX/PDF exporters
                 or local template                         (formatting/exporters.py)
```

## Component responsibilities

- **Streamlit (`app.py`):** collects details, posts generation requests, keeps the editable draft in session state, and requests file exports.
- **FastAPI (`main.py`, `routes.py`):** provides health, generation, and export endpoints and validates request data with Pydantic.
- **AI core (`ai_core/gemini_generator.py`):** builds the drafting prompt, calls Google's `google-genai` SDK when configured, or builds a visibly labeled local template.
- **Formatting (`formatting/exporters.py`):** creates plain text, branded Word documents, and paginated branded PDF files.
- **Configuration:** `.env.example` documents settings; `.env` is local-only and ignored by Git.

## API design

| Method | Route | Purpose |
|---|---|---|
| GET | `/` | API root and documentation link. |
| GET | `/health` | Health status. |
| POST | `/generate` | Generate an AI or local template draft. |
| POST | `/export/txt` | Export provided content as text. |
| POST | `/export/docx` | Export provided content as Word. |
| POST | `/export/pdf` | Export provided content as PDF. |

Interactive API documentation is available at `/docs` while the backend runs.

## Key design choices

- The API owns generation and formatting so the frontend stays focused on interaction.
- The frontend sends edited content to export endpoints, ensuring downloads contain the visible edits.
- Drafts are held in the Streamlit session; there is no database in the initial version.
- The Gemini key remains on the backend and is not sent to the browser.
- Missing legal information should be surfaced as a placeholder instead of invented specifics.

## Phase outcome

The component boundaries, data flow, and API surface are defined. Implementation details are tracked in [Phase 5: Project Development](05-project-development.md).
