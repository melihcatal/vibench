from __future__ import annotations

from typing import List, Optional

from document_client import load_document_input, textract_bytes_payload, textract_client
from document_models import LayoutBlock, normalize_blocks


def extract_layout(image_path: Optional[str] = None, content: Optional[bytes] = None, mime_type: str = "image/png") -> List[LayoutBlock]:
    document = load_document_input(content=content, path=image_path, mime_type=mime_type)
    client = textract_client()
    response = client.analyze_document(Document=textract_bytes_payload(document), FeatureTypes=["LAYOUT"])
    blocks = [
        {"type": b.get("BlockType"), "text": b.get("Text", ""), "confidence": b.get("Confidence"), "raw": b}
        for b in response.get("Blocks", [])
        if b.get("BlockType") in {"LAYOUT_TEXT", "LAYOUT_TITLE", "LAYOUT_HEADER", "LAYOUT_FOOTER", "LAYOUT_LIST", "LAYOUT_TABLE", "LAYOUT_KEY_VALUE", "LAYOUT_SECTION_TITLE"}
    ]
    return normalize_blocks(blocks)
