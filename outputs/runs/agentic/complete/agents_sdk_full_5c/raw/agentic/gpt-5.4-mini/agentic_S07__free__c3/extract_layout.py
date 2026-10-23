from __future__ import annotations

from typing import List

from document_client import DocumentAiConfig, build_document_ai_client, build_process_request
from document_models import LayoutElement, normalize_document_ai_text


def extract_layout(image_bytes: bytes, mime_type: str = "image/png") -> List[LayoutElement]:
    config = DocumentAiConfig()
    client = build_document_ai_client(config.endpoint)
    request = build_process_request(image_bytes, mime_type=mime_type, config=config)
    response = client.process_document(request=request)
    document = response.document
    elements: List[LayoutElement] = []
    for page in document.pages:
        for block in getattr(page, "blocks", []):
            text = normalize_document_ai_text(documentai_text(document, block.layout.text_anchor))
            elements.append(LayoutElement(kind="block", text=text, confidence=float(block.layout.confidence or 0.0)))
        for line in getattr(page, "lines", []):
            text = normalize_document_ai_text(documentai_text(document, line.layout.text_anchor))
            elements.append(LayoutElement(kind="line", text=text, confidence=float(line.layout.confidence or 0.0)))
        for table in getattr(page, "tables", []):
            elements.append(LayoutElement(kind="table", text="table detected", confidence=float(table.layout.confidence or 0.0)))
    return elements


def documentai_text(document, text_anchor):
    from google.cloud import documentai

    return documentai.Document.TextAnchor.get_text(text_anchor, document.text)
