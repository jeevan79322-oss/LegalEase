# Phase 5: Project Development

## Implemented structure

```text
app.py                         Streamlit interface
main.py                        FastAPI app
routes.py                      Health, generate, and export endpoints
ai_core/gemini_generator.py    Gemini integration and local fallback
formatting/exporters.py        TXT, DOCX, and PDF creation
assets/legalease_logo.png      Interface and document brand mark
.env.example                   Configuration template
requirements.txt               Python dependencies
.vscode/                       VS Code configuration and tasks
Dockerfile                     Container image definition
docker-compose.yml             Local two-service setup
docs/phases/                   Phase-wise project records
```

## User workflow

1. Enter the document type, parties, terms, effective date, and optional jurisdiction/language.
2. Submit the form to the API.
3. Receive a Gemini-generated draft if configured, otherwise a local template draft.
4. Edit the content in the preview.
5. Download the edited version as TXT, DOCX, or PDF.

## AI integration

The backend uses the Google `google-genai` SDK. `GEMINI_API_KEY` enables provider calls and `GEMINI_MODEL` selects the model. The default model setting in `.env.example` is `gemini-3.8-flash`; users can change it to a model available to their API account. Without a key, the generator returns a structured local template and marks it as non-AI output.

The drafting prompt requests formal, numbered sections, signature blocks, placeholders for unknown facts, and no claims of enforceability. This prompt does not guarantee legal accuracy.

## Configuration and run commands

Create a virtual environment, install dependencies, and copy `.env.example` to `.env`. Start the API and UI in separate terminals:

```cmd
.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
.venv\Scripts\python.exe -m streamlit run app.py
```

The UI is normally at `http://localhost:8501`; API docs are at `http://127.0.0.1:8000/docs`.

## Phase outcome

The core application and local deployment setup have been implemented. See [Phase 7: Project Documentation](07-project-documentation.md) for the user-facing guide inventory.
