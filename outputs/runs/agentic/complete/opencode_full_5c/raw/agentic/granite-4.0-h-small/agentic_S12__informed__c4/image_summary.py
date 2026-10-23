import json
import os
from vision_models import VisionResponseNormalization
from typing import List, Dict


def summarize_visual_analysis(results: Dict) -> Dict:
    """Summarize results from label detection, description, text detection, and safety check.

    Args:
        results: dict returned by workflow orchestrator containing keys:
            - labels: list of detected labels
            - description: visual description
            - texts: list of extracted OCR texts
            - safe: boolean safety flag

    Returns:
        A concise summary dict ready for downstream consumption.
    """
    # Normalize even if raw values are already in expected form
    labels = VisionResponseNormalization.normalize_labels(results.get("labels", []))
    description = VisionResponseNormalization.normalize_description(
        results.get("description", "")
    )
    texts = VisionResponseNormalization.normalize_text(results.get("texts", []))
    safe = VisionResponseNormalization.normalize_safety(results.get("safe", True))

    summary = {
        "image": results.get("image_path", "unknown_image.jpg"),
        "labels": labels,
        "description": description,
        "extracted_texts": texts,
        "safe": safe,
    }
    return summary
