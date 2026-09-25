"""HTTP endpoints for drafting and exporting documents."""
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from pydantic import BaseModel, Field
from ai_core.gemini_generator import GeminiDocumentGenerator, GenerationError
from formatting.exporters import make_docx, make_pdf, make_txt

router = APIRouter()

class DocumentRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=100)
    parties: str = Field(min_length=2, max_length=2000)
    terms: list[str] = Field(min_length=1, max_length=30)
    effective_date: str = Field(min_length=2, max_length=100)
    jurisdiction: str = Field(default="Not specified", max_length=100)
    language: str = Field(default="English", min_length=2, max_length=40)

class ExportRequest(BaseModel):
    document_type: str = Field(min_length=2, max_length=100)
    content: str = Field(min_length=1, max_length=100_000)

@router.get("/health", tags=["health"])
def health() -> dict[str, str]:
    return {"status": "ok"}

@router.post("/generate", tags=["documents"])
def generate_document(payload: DocumentRequest) -> dict[str, str | bool]:
    try:
        result = GeminiDocumentGenerator().generate_document(payload)
    except GenerationError as exc:
        raise HTTPException(status_code=503, detail=str(exc)) from exc
    except Exception as exc:
        raise HTTPException(status_code=502, detail="The AI provider could not complete the request.") from exc
    return {"content": result.content, "ai_generated": result.ai_generated, "model": result.model}

@router.post("/export/{file_format}", tags=["documents"])
def export_document(file_format: str, payload: ExportRequest) -> Response:
    builders = {
        "txt": (make_txt, "text/plain; charset=utf-8"),
        "docx": (make_docx, "application/vnd.openxmlformats-officedocument.wordprocessingml.document"),
        "pdf": (make_pdf, "application/pdf"),
    }
    selected = builders.get(file_format.lower())
    if selected is None:
        raise HTTPException(status_code=400, detail="Format must be txt, docx, or pdf.")
    builder, media_type = selected
    extension = file_format.lower()
    return Response(content=builder(payload.content, payload.document_type), media_type=media_type,
                    headers={"Content-Disposition": f'attachment; filename="legalease-draft.{extension}"'})
