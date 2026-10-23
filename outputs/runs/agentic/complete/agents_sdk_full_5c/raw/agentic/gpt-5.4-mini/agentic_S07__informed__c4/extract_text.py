from __future__ import annotations

from document_client import DocumentAIClientHelper
from document_models import DocumentRequest, TextResult, normalize_text


def extract_text(file_path: str, mime_type: str = "image/png") -> TextResult:
    helper = DocumentAIClientHelper()
    response = helper.process(DocumentRequest(file_path=file_path, mime_type=mime_type))
    document = response.document
    text = normalize_text(getattr(document, "text", ""))
    pages = [normalize_text(getattr(page, "layout", {}).get("text_anchor", {})) for page in getattr(document, "pages", [])]
    return TextResult(text=text, pages=pages, raw=response)
