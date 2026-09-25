# Phase 4: Project Planning

## Work breakdown

| Workstream | Deliverable | Status |
|---|---|---|
| Ideation | Use cases, scope, and responsible-use boundaries | Complete |
| Requirements | Inputs, outputs, constraints, and acceptance criteria | Complete |
| Design | Frontend/backend/AI/exporter architecture | Complete |
| Development | Streamlit, FastAPI, Gemini adapter, template mode, exports | Implemented |
| Verification | API, generation fallback, export, and UI smoke checks | Completed locally; live Gemini requires a key |
| Documentation | Setup, configuration, API, and phase records | In progress with these phase files |
| Demonstration | Local walkthrough and sample agreement | Planned for presenter |

## Milestones

1. Establish project structure and configuration.
2. Implement backend API and health checks.
3. Integrate the Gemini SDK and local fallback.
4. Build the guided Streamlit form and editable preview.
5. Add TXT, DOCX, and PDF export.
6. Verify local end-to-end behavior and prepare user documentation.
7. Demonstrate the application with non-sensitive example data.

## Dependencies and risks

- **Gemini credentials and quota:** use template mode until a key is configured; live generation depends on external availability.
- **Legal accuracy:** drafts can be incomplete or incorrect; label them as drafts and require qualified review.
- **Sensitive data:** do not enter sensitive personal information; configured Gemini use sends prompt data to Google.
- **Public deployment:** current API has no authentication or rate limiting and is intended for local use.

## Definition of done

- Required workflows are implemented and manually checked.
- Setup instructions work from a clean Python virtual environment.
- Secrets are not committed.
- Known limitations and future work are documented.

## Phase outcome

The work is sequenced into seven implementation milestones, with security, AI availability, and legal accuracy called out as project risks. See [Phase 6: Project Testing](06-project-testing.md) for verification evidence.
