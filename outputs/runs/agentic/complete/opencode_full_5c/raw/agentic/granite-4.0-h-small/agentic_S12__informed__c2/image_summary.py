# [LATER-STEP] image_summary.py

from typing import List, Dict
from vision_models import (
    ImageDescription,
    DetectedLabel,
    DetectedText,
    SafetyEvaluation,
)


def summarize_visual_analysis(
    labels: List[DetectedLabel],
    description: ImageDescription,
    text: List[DetectedText],
    safety: SafetyEvaluation,
) -> Dict:
    """
    Combine results from all same-scenario steps into a concise JSON summary.
    """
    return {
        "labels": [{"name": l.name, "confidence": l.confidence} for l in labels],
        "description": {
            "text": description.text,
            "confidence": description.confidence,
        },
        "text": [{"text": t.text, "bounding_box": t.bounding_box} for t in text],
        "safety": {
            "unsafe": safety.unsafe,
            "issues": safety.issues,
        },
    }
