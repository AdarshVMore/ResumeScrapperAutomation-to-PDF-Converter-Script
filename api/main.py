from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import Response
from pydantic import BaseModel, Field

from api.config import MAX_HTML_SIZE
from api.pdf_service import html_to_pdf
from api.storage_service import upload_pdf

app = FastAPI(title="HTML to PDF API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class PDFRequest(BaseModel):
    html: str
    filename: str = Field(default="output.pdf")


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/generate-pdf")
def generate_pdf(req: PDFRequest):
    if len(req.html.encode("utf-8")) > MAX_HTML_SIZE:
        raise HTTPException(status_code=413, detail="HTML content exceeds 5MB limit")

    if not req.filename.endswith(".pdf"):
        req.filename += ".pdf"

    # Generate PDF
    try:
        pdf_bytes = html_to_pdf(req.html)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

    # Upload to Supabase
    try:
        storage_url = upload_pdf(pdf_bytes, req.filename)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Storage upload failed: {str(e)}")

    return Response(
        content=pdf_bytes,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="{req.filename}"',
            "X-Storage-URL": storage_url,
        },
    )
