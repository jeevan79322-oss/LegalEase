"""LegalEase FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import router

app = FastAPI(title="LegalEase API", description="Draft legal documents with AI and export editable files.", version="1.0.0")
app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:8501", "http://127.0.0.1:8501"], allow_credentials=False, allow_methods=["GET", "POST"], allow_headers=["*"])
app.include_router(router)

@app.get("/", tags=["health"])
def root() -> dict[str, str]:
    return {"name": "LegalEase API", "status": "ok", "docs": "/docs"}
