from __future__ import annotations

from document_client import analyze_document, get_client
from document_models import DocumentInput, LayoutBlock, normalize_blocks

PROVIDER = "Azure AI Document Intelligence"
MODEL_ID = "prebuilt-layout"


def extract_layout(document_bytes: bytes, mime_type: str = "image/png") -> list[LayoutBlock]:
    client = get_client()
    document = DocumentInput(content=document_bytes, mime_type=mime_type)
    result = analyze_document(client, document, model_id=MODEL_ID)
    raw_blocks = []
    for page in getattr(result, "pages", []):
        for line in getattr(page, "lines", []):
            raw_blocks.append({"kind": "line", "text": getattr(line, "content", ""), "bounding_box": getattr(line, "polygon", None)})
    for paragraph in getattr(result, "paragraphs", []):
        raw_blocks.append({"kind": "paragraph", "text": getattr(paragraph, "content", ""), "bounding_box": getattr(paragraph, "bounding_regions", None)})
    return normalize_blocks(raw_blocks)
