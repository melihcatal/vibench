# vision_models.py
"""Local request, response, and normalization helpers for Static Image and Visual Understanding.

Encapsulates request building, result parsing, and consistency across providers.
"""

from typing import Any, Dict, List

# Normalized representation of detected labels
NormalizedLabel = Dict[str, Any]


def normalize_labels(provider_name: str, raw: Any) -> List[NormalizedLabel]:
    """Convert provider‑specific label output to a common schema.

    Schema:
        [
            {"name": str, "confidence": float},
            ...
        ]
    """
    if provider_name == "azure":
        # Azure AI Vision returns a list of Label objects with .name and .confidence
        return [{"name": lbl.name, "confidence": float(lbl.confidence)} for lbl in raw]
    elif provider_name == "google":
        # Google Vision returns a list of EntityAnnotation with .description and .score
        return [
            {"name": ent.description, "confidence": float(ent.score)} for ent in raw
        ]
    elif provider_name == "openai":
        # OpenAI Gemini response is free‑form text; we treat whole text as one label
        text = raw.get("content", "")
        return [{"name": text.strip(), "confidence": 1.0}]
    else:
        raise ValueError(f"Unsupported provider for normalization: {provider_name}")


def normalize_ocr(provider_name: str, raw: Any) -> List[str]:
    """Convert provider‑specific OCR output to a list of extracted text strings.

    Returns:
        List of plain text segments.
    """
    if provider_name == "google":
        # Google Vision OCR returns a .description field per block
        return [block.description for block in raw]
    else:
        raise ValueError(f"Unsupported provider for OCR: {provider_name}")
