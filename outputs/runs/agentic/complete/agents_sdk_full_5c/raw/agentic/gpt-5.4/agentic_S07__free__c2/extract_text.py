from __future__ import annotations

from document_client import process_document
from document_models import TextExtractionResult


def extract_text(file_path: str) -> TextExtractionResult:
    document = process_document(file_path)
    pages = []
    for page in document.pages:
        pages.append(
            {
                "page_number": int(page.page_number),
                "dimension": {
                    "width": float(page.dimension.width),
                    "height": float(page.dimension.height),
                    "unit": page.dimension.unit,
                },
            }
        )
    return TextExtractionResult(text=document.text or "", pages=pages)
