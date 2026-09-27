import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError("GEMINI_API_KEY is not set in the .env file")


class GeminiDocumentGenerator:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)

    def generate_document(self, document_type, parties, terms, dates):
        prompt = f"""
Create a professional legal document.

Document Type:
{document_type}

Parties Involved:
{parties}

Terms and Conditions:
{terms}

Effective Date:
{dates}

Requirements:
- Use clear and professional legal language.
- Include a title.
- Include the parties and effective date.
- Organize the document into appropriate sections.
- Include the provided terms and conditions.
- Do not invent important personal or financial information. Use the exact values provided above for Document Type, Parties Involved, Terms and Conditions, and Effective Date. Do not replace them with placeholders.
- Make the document editable and well structured.
- Add a final signature section.

This document is generated for drafting and informational purposes
and should be reviewed by a qualified legal professional before use.
"""

        response = self.client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )

        return response.text
