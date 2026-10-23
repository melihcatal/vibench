from __future__ import annotations

from typing import Optional

from document_client import get_textract_client
from document_models import OCRTextResult


def extract_text(image_bytes: bytes, mime_type: str = "image/png", region_name: Optional[str] = None) -> OCRTextResult:
    helper = get_textract_client(region_name=region_name)
    response = helper.client.detect_document_text(Document={"Bytes": image_bytes})
    lines = []
    confidence_values = []
    for block in response.get("Blocks", []):
        if block.get("BlockType") == "LINE":
            lines.append(block.get("Text", ""))
            if "Confidence" in block:
                confidence_values.append(float(block["Confidence"]))
    text = "\n".join(lines)
    confidence = sum(confidence_values) / len(confidence_values) if confidence_values else None
    return OCRTextResult(text=text, pages=[], confidence=confidence, raw=response)
