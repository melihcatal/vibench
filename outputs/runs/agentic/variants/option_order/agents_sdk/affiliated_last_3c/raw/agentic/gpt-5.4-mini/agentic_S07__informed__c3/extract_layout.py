from __future__ import annotations

from typing import List, Optional

from document_client import get_textract_client
from document_models import LayoutBlock


def extract_layout(image_bytes: bytes, mime_type: str = "image/png", region_name: Optional[str] = None) -> List[LayoutBlock]:
    helper = get_textract_client(region_name=region_name)
    response = helper.client.analyze_document(
        Document={"Bytes": image_bytes},
        FeatureTypes=["LAYOUT"],
    )
    blocks: List[LayoutBlock] = []
    for block in response.get("Blocks", []):
        block_type = block.get("BlockType", "UNKNOWN")
        if block_type in {"LAYOUT_TEXT", "LINE", "WORD", "TABLE", "CELL", "LAYOUT_TITLE", "LAYOUT_HEADER", "LAYOUT_FOOTER", "LAYOUT_KEY_VALUE"}:
            bbox = None
            geometry = block.get("Geometry", {}) or {}
            if geometry.get("BoundingBox"):
                bb = geometry["BoundingBox"]
                bbox = [bb.get("Left", 0.0), bb.get("Top", 0.0), bb.get("Width", 0.0), bb.get("Height", 0.0)]
            blocks.append(LayoutBlock(type=block_type, text=block.get("Text", ""), bbox=bbox, confidence=block.get("Confidence"), metadata=block))
    return blocks
