from __future__ import annotations

from document_client import analyze_document, get_client
from document_models import DocumentInput, OCRTextResponse, normalize_text

PROVIDER = "Azure AI Document Intelligence"
MODEL_ID = "prebuilt-read"


def extract_text(image_bytes: bytes, mime_type: str = "image/png") -> OCRTextResponse:
    client = get_client()
    document = DocumentInput(content=image_bytes, mime_type=mime_type)
    result = analyze_document(client, document, model_id=MODEL_ID)
    text = normalize_text(getattr(result, "content", getattr(result, "text", "")))
    if not text and hasattr(result, "pages"):
        text = normalize_text([getattr(line, "content", "") for page in result.pages for line in getattr(page, "lines", [])])
    return OCRTextResponse(text=text, raw=result)
