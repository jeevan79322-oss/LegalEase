# LegalEase

LegalEase is a local-first legal document drafting application. It includes a Streamlit interface, a FastAPI backend, optional Gemini drafting, an editable text preview, and TXT, DOCX, and PDF exports.

> **Drafting tool only:** LegalEase does not provide legal advice, verify legal validity, or guarantee compliance with local law. Have a qualified lawyer review a draft before relying on or signing it. Do not enter highly sensitive personal information.

## Features

- Draft NDAs, employment agreements, leases, service agreements, or a custom document.
- Capture parties, terms, effective date, jurisdiction, and output language.
- Use Gemini through the current `google-genai` SDK when an API key is configured.
- Run immediately without a key using an explicitly labeled local template draft.
- Edit the generated text before exporting to TXT, Word, or PDF.
- Generate documents through the REST API; explore it at `http://127.0.0.1:8000/docs`.
- Keep draft content in the browser session; this application does not save documents to a database.
- When a Gemini key is configured, agreement details are sent to Google for generation under the Gemini API service terms. Without a key, drafting stays local.

## Requirements

- Python 3.10 or newer (Python 3.11 or 3.12 recommended).
- VS Code with the Python extension.
- A Gemini API key only if you want AI-generated content. Create one in [Google AI Studio](https://aistudio.google.com/apikey).

## Setup in VS Code (Windows PowerShell)

1. Open this project folder in VS Code.
2. Open **Terminal → New Terminal** and create a virtual environment:

   ```powershell
   py -3 -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

   If PowerShell blocks activation, run `Set-ExecutionPolicy -Scope Process Bypass` in that terminal, then activate again. You can also use `.venv\Scripts\python.exe` directly without activation.

3. Install dependencies:

   ```powershell
   python -m pip install --upgrade pip
   pip install -r requirements.txt
   ```

4. Copy `.env.example` to `.env`. Leave `GEMINI_API_KEY` empty to use local template mode, or paste your AI Studio key after `GEMINI_API_KEY=`. Keep `.env` private; it is excluded from Git.

5. Start the API in the first terminal:

   ```powershell
   .\.venv\Scripts\python.exe -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
   ```

6. Start the interface in a second terminal:

   ```powershell
   .\.venv\Scripts\python.exe -m streamlit run app.py
   ```

7. Open the Streamlit URL printed in the terminal (usually `http://localhost:8501`). The API health endpoint is `http://127.0.0.1:8000/health`; interactive API documentation is at `http://127.0.0.1:8000/docs`.

### Optional VS Code task shortcuts

After creating `.venv`, open **Terminal → Run Task…** and run **LegalEase: API** and **LegalEase: Frontend** in separate terminals. The tasks use the project virtual environment.

## Run with Docker

Create `.env` as above, then run:

```powershell
docker compose up --build
```

Open `http://localhost:8501`. Stop the services with Ctrl+C, then optionally run `docker compose down`.

## Test the application manually

1. Open the frontend, choose a document type, enter parties, an effective date, jurisdiction, and one or more terms.
2. Select **Generate draft**. With no key, confirm that the interface labels the result **Local template mode**. With a valid key, it identifies the configured Gemini model.
3. Change some text in the preview and download each of TXT, DOCX, and PDF. Open the Word/PDF files to check their layout and confirm the edited text is included.
4. Visit `/health` and `/docs` to confirm the API is running. In `/docs`, `POST /generate` accepts JSON such as:

   ```json
   {
     "document_type": "Non-disclosure agreement",
     "parties": "Jordan Lee (Consultant); Northstar Studio Ltd. (Client)",
     "terms": ["Use confidential information only for evaluating the project", "Return materials when discussions end"],
     "effective_date": "1 October 2026",
     "jurisdiction": "Ontario, Canada",
     "language": "English"
   }
   ```

## Configuration

| Variable | Default | Purpose |
|---|---|---|
| `GEMINI_API_KEY` | empty | Enables Gemini generation; when absent, the API returns a local template draft. |
| `GEMINI_MODEL` | `gemini-3.8-flash` | Gemini model name; change it in `.env` if your account uses another available model. |
| `LEGALEASE_API_URL` | `http://127.0.0.1:8000` | Backend URL used by Streamlit. Docker Compose sets this to `http://api:8000`. |

## Project structure

```text
LegalEase/
├── ai_core/gemini_generator.py  # Gemini and local template drafting
├── formatting/exporters.py      # TXT, DOCX, PDF export
├── assets/legalease_logo.png    # Document and interface branding
├── .vscode/                     # VS Code recommendations and run tasks
├── app.py                       # Streamlit frontend
├── main.py                      # FastAPI setup and health route
├── routes.py                    # Generate and export API routes
├── requirements.txt
├── .env.example
├── Dockerfile
└── docker-compose.yml
```

## Troubleshooting

- **Frontend cannot reach backend:** Make sure the API terminal is running on port 8000. If it is hosted elsewhere, set `LEGALEASE_API_URL` before starting Streamlit.
- **Gemini unavailable:** Check the API key, enabled Gemini API access, quota/billing, and `GEMINI_MODEL`. If the key is empty, local template mode is expected.
- **PowerShell activation error:** Use the process-scoped execution-policy command in the setup section, or invoke `.venv\Scripts\python.exe` directly.
- **Port already in use:** Stop the other process or select a different port and update the frontend's `LEGALEASE_API_URL` accordingly.

## Deployment notes

The included Docker Compose setup is intended for local use. Before public deployment, add authentication, rate limiting, HTTPS, secret management, privacy/retention controls, monitoring, and an appropriate legal review. Do not expose the unauthenticated API directly to the public internet.
