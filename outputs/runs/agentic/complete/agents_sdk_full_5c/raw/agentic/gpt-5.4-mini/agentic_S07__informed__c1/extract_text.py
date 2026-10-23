from __future__ import annotations

from typing import Optional

from document_client import load_document_input, textract_bytes_payload, textract_client
from document_models import OCRResult, normalize_text


def extract_text(image_path: Optional[str] = None, content: Optional[bytes] = None, mime_type: str = "image/png") -> OCRResult:
    document = load_document_input(content=content, path=image_path, mime_type=mime_type)
    client = textract_client()
    response = client.detect_document_text(Document=textract_bytes_payload(document))
    lines = []
    pages = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            lines.append(block.get("Text", ""))
        if block.get("BlockType") == "PAGE":
            pages.append(block)
    return OCRResult(text=normalize_text("\n".join(lines)), pages=pages, raw=response)
