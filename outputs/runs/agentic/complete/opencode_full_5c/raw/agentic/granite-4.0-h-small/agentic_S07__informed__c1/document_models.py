# Local type models and normalization helpers for OCR and layout pipelines

from typing import Any, Dict, List

# Type aliases for OCR results
OcrText = List[str]
OcrConfidence = List[float]

# Normalized OCR response model (same shape for any provider)
NormalizedOcrResult = Dict[str, Any]

# Layout block types (example)
LayoutBlockType = str
LayoutBlock = Dict[str, Any]
LayoutResult = List[LayoutBlock]

# Helper to normalize raw provider responses to a common shape used downstream

ormalize_ocr = lambda raw: {
    "text": [
        block["Text"] for block in raw.get("Blocks", []) if block["BlockType"] == "LINE"
    ],
    "confidence": [
        block.get("Confidence", 0)
        for block in raw.get("Blocks", [])
        if block["BlockType"] == "LINE"
    ],
}

ormalize_layout = lambda raw: [
    {
        "type": block["BlockType"],
        "geometry": block.get("Geometry", {}),
        "content": block.get("Text", ""),
    }
    for block in raw.get("Blocks", [])
]
