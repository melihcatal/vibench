# extract_layout.py
import os
from typing import Any, List, Dict

# Local helpers
from document_client import document_client
from document_models import OCRRequest, OCRResult, LayoutElement, LayoutResult

# Google Document AI constants (processor ID for General Document OCR)
DOC_AI_ENDPOINT = os.getenv('GOOGLE_DOCUMENTAI_ENDPOINT', 'https://documentai.googleapis.com/v1/projects/{project_id}/locations/us-central1/processors/{processor_id}')

# Example processor ID placeholder; replace with your own processor resource name
DEFAULT_PROCESSOR_ID = 'a12345b6c7d8e9f0g1h2i3j4k5l6m7n8o9p0'


def extract_layout(file_path: str) -> LayoutResult:
    """Extract layout elements (lines, words, tables, etc.) from a PDF/JPEG using Google Document AI."""
    # Build the fully qualified processor name
    processor_name = (
        f"projects/{os.getenv('GOOGLE_CLOUD_PROJECT')}/locations/us-central1/processors/"
        f"{DEFAULT_PROCESSOR_ID}"
    )

    with open(file_path, 'rb') as f:
        raw_bytes = f.read()

    # Call the helper client
    response = document_client.process_document(name=processor_name, raw_bytes=raw_bytes)
    # Process response into our layout model
    pages = []
    for page in response.document.pages:
        for entity in page.entities:
            # Simplified; in practice you would differentiate by entity type
            element = LayoutElement(
                page_number=page.page_number,
                type=entity.type,
                text=entity.text,
                confidence=entity.confidence,
                bounding_box=dict(entity.layout.bounding_poly.normalized_vertices[0]),
            )
            pages.append(element)
    return LayoutResult(document_id=os.path.basename(file_path), pages=pages, entities=response.document.pages)

if __name__ == '__main__':
    # quick test (remove in production)
    result = extract_layout('sample.pdf')
    print(result)