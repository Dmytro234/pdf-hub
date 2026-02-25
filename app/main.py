from fastapi import FastAPI

from app.api.pdf_routes import router as pdf_router

tags_metadata = [
    {"name": "Health", "description": "Service health endpoints"},
    {"name": "PDF • Merge", "description": "Combine multiple PDFs into one"},
    {"name": "PDF • Split", "description": "Split PDFs by pages/range/custom list"},
    {"name": "PDF • Compress", "description": "Reduce PDF size via Ghostscript"},
    {"name": "PDF • Convert", "description": "DOCX↔PDF and Images→PDF"},
    {"name": "PDF • Security", "description": "Encrypt/decrypt and permissions"},
]

app = FastAPI(
    title="PDF Hub API",
    description="Internal PDF tools: merge, split, compress, convert, encrypt/decrypt.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.include_router(pdf_router)


@app.get("/health", tags=["Health"], summary="Health check")
def health():
    return {"status": "ok"}
