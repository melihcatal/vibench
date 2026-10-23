from __future__ import annotations

from document_client import process_document
from document_models import TextExtractionResult


PROVIDER = "google-document-ai"


def extract_text(source: str, mime_type: str | None = None) -> TextExtractionResult:
    document = process_document(source=source, mime_type=mime_type)
    language = None
    if getattr(document, "pages", None):
        for page in document.pages:
            if getattr(page, "detected_languages", None):
                language = page.detected_languages[0].language_code
                break
    return TextExtractionResult(text=document.text or "", language=language, raw={"uri": "https://cloud.google.com/document-ai"})
