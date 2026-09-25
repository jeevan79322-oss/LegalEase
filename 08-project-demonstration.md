# Phase 8: Project Demonstration

## Demonstration objective

Show how LegalEase converts structured agreement details into an editable draft, then exports the edited content in common file formats.

## Before the demo

1. Install dependencies from `requirements.txt` in a virtual environment.
2. Optionally configure `GEMINI_API_KEY` in a local `.env` file. Do not expose the key in screenshots or commits.
3. Start FastAPI on port 8000 and Streamlit on port 8501 in separate terminals.
4. Use fictional parties and non-sensitive sample terms.

## Suggested walkthrough

1. Open `http://localhost:8501` and introduce the document studio.
2. Select “Non-disclosure agreement”.
3. Enter fictional parties, an effective date, and terms such as purpose-limited use of confidential information and return of materials.
4. Generate a draft and explain the AI label or local-template label.
5. Edit a clause in the preview.
6. Download TXT, DOCX, and PDF; open one or more files and point out the branding and editable text.
7. Show the API health page and `/docs` if the audience wants to see the service interface.
8. Close with the limitations: this is a starting draft, not legal advice; verify all terms with a qualified lawyer.

## Demo success criteria

- The interface loads and the API responds.
- The audience sees a clearly labeled AI or local-template result.
- A visible edit is reflected in the exported document.
- The presenter explains that legal validity and jurisdictional compliance are not guaranteed.

## Demo troubleshooting

- If the UI reports a backend connection problem, confirm that Uvicorn is still running on port 8000.
- If Gemini is unavailable, leave the key unset and demonstrate the local template mode.
- If a port is already occupied, stop the conflicting process or update the configured ports and API URL.

## Phase outcome

The walkthrough can be completed locally without an AI credential. A live Gemini demonstration requires a valid key and available model quota. Do not use real confidential agreements in a public presentation.
