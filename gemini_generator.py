"""Gemini-backed legal drafting, with a local template mode for setup."""
from dataclasses import dataclass
import os
from dotenv import load_dotenv

load_dotenv()

class GenerationError(RuntimeError):
    """Raised when a configured AI provider cannot generate a response."""

@dataclass
class GeneratedDocument:
    content: str
    ai_generated: bool
    model: str

class GeminiDocumentGenerator:
    def __init__(self) -> None:
        self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
        self.model_name = os.getenv("GEMINI_MODEL", "gemini-3.8-flash").strip()

    @staticmethod
    def _prompt(payload: object) -> str:
        terms = "\n".join(f"- {term}" for term in payload.terms)
        return f"""Draft a clear, structured first draft of the requested legal document.
This is general drafting assistance, not legal advice. Do not claim the document is legally valid, enforceable, or compliant. Do not invent facts, statutory references, notice periods, or remedies. Where important information is missing, use [BRACKETED PLACEHOLDER] and identify it in a short 'Items to confirm' section. Use plain, formal language and numbered sections. Include a signature block for each party. Do not include commentary about being an AI.

Document type: {payload.document_type}
Parties and roles: {payload.parties}
Effective date: {payload.effective_date}
Jurisdiction: {payload.jurisdiction}
Language: {payload.language}
Requested terms (preserve meaning; do not add unsupported specifics):
{terms}
"""

    @staticmethod
    def _local_draft(payload: object) -> str:
        terms = "\n".join(f"{i}. {term}" for i, term in enumerate(payload.terms, 1))
        return (
            f"{payload.document_type.upper()}\n\n"
            f"Effective date: {payload.effective_date}\nJurisdiction: {payload.jurisdiction}\n\n"
            f"PARTIES\n{payload.parties}\n\n"
            "1. PURPOSE AND SCOPE\nThe parties intend to enter into this agreement on the terms set out below. [Describe the agreed purpose and scope.]\n\n"
            f"2. AGREED TERMS\n{terms}\n\n"
            "3. GENERAL\nThe parties should review this draft, complete all bracketed fields, and obtain advice on local requirements before signing.\n\n"
            "SIGNATURES\n\nParty 1: __________________________  Date: ______________\n\nParty 2: __________________________  Date: ______________\n\n"
            "ITEMS TO CONFIRM\nAdd any missing commercial details, notice method, governing law, and other terms required for this transaction.\n\n"
            "DRAFTING NOTICE: This is a starting point for discussion, not legal advice or a guarantee of legal validity."
        )

    def generate_document(self, payload: object) -> GeneratedDocument:
        if not self.api_key:
            return GeneratedDocument(self._local_draft(payload), False, "local-template")
        try:
            from google import genai
            client = genai.Client(api_key=self.api_key)
            response = client.models.generate_content(
                model=self.model_name,
                contents=self._prompt(payload),
                config={"temperature": 0.25, "max_output_tokens": 5000},
            )
            text = (response.text or "").strip()
            if not text:
                raise GenerationError("The AI provider returned an empty draft. Please try again.")
            return GeneratedDocument(text, True, self.model_name)
        except GenerationError:
            raise
        except Exception as exc:
            raise GenerationError("Gemini could not generate the draft. Check your API key, model setting, quota, and network connection.") from exc
