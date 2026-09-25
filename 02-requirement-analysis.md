# Phase 2: Requirement Analysis

## Stakeholders and needs

| Stakeholder | Need |
|---|---|
| Individual user | Enter agreement details and receive a usable starting draft. |
| Small organization | Edit wording and save copies in familiar file formats. |
| Project maintainer | Configure the AI provider without putting keys in source control. |
| Reviewer | Understand assumptions, missing details, and limitations of a draft. |

## Functional requirements

1. Provide a form for document type, parties, terms, effective date, jurisdiction, and language.
2. Validate required fields before generation.
3. Generate content through Gemini when a key is configured.
4. Provide a labeled local template draft when no Gemini key is present.
5. Show the complete draft in an editable preview.
6. Export the edited content as TXT, DOCX, and PDF.
7. Expose API health, generation, and export routes through FastAPI.

## Quality and operational requirements

- Store the Gemini key in an environment file that is excluded from Git.
- Avoid database persistence in the initial local application.
- Clearly communicate that the tool does not provide legal advice or certify compliance.
- Run the frontend and backend locally using documented commands.
- Keep AI model selection configurable through `GEMINI_MODEL`.

## Input and output

**Inputs:** document type, parties and roles, one or more terms, effective date, jurisdiction, and language.

**Outputs:** editable draft text and downloadable TXT, DOCX, or PDF files.

## Constraints and assumptions

- Users supply accurate party and transaction details.
- Jurisdiction-specific legal validity is not evaluated.
- Gemini generation requires a valid API key, model access, quota, and network connectivity.
- Local template mode is a structured outline and is not equivalent to AI drafting.

## Acceptance criteria

- Missing required inputs receive an actionable message.
- The app can generate a local draft without an API key.
- Configured Gemini errors are shown as errors rather than silently replaced by a template.
- Edited text is present in every downloaded format.
- DOCX and PDF have readable branded layouts.

## Phase outcome

The initial feature and quality requirements are defined. Product boundaries and constraints feed into [Phase 3: Project Design](03-project-design.md).
