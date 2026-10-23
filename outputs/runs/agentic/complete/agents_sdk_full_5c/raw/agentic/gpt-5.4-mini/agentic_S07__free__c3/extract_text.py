from __future__ import annotations

from google.cloud import documentai

from document_client import DocumentAiConfig, build_document_ai_client, build_process_request
from document_models import OCRBlock, OCRResponse, normalize_document_ai_text


def extract_text(image_bytes: bytes, mime_type: str = "image/png") -> OCRResponse:
    config = DocumentAiConfig()
    client = build_document_ai_client(config.endpoint)
    request = build_process_request(image_bytes, mime_type=mime_type, config=config)
    response = client.process_document(request=request)
    document = response.document
    full_text = normalize_document_ai_text(document.text or "")
    blocks = []
    for page in document.pages:
        for paragraph in getattr(page, "paragraphs", []):
            text_anchor = paragraph.layout.text_anchor
            paragraph_text = documentai.Document.TextAnchor.get_text(paragraph.layout.text_anchor, document.text)
            blocks.append(OCRBlock(text=normalize_document_ai_text(paragraph_text), confidence=float(paragraph.layout.confidence or 0.0)))
    return OCRResponse(text=full_text, blocks=blocks, raw=response.__class__.__name__ and {"processor": config.processor_name})
