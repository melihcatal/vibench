# [LATER-STEP] visual_safety_text.py

import os
from safety_client import SafetyClient
from vision_models import VisionResponseNormalization, normalize_vision_response


def verify_caption_safety(caption: str) -> bool:
    """Check whether a generated caption contains unsafe language using a safety service.

    Returns True if safe, False otherwise.
    """
    client = SafetyClient()
    # Most safety APIs expose a simple `check` method returning a bool or risk score.
    return client.is_safe(caption)


def filter_unsafe_labels(
    labels: List[str], unsafe: VisionResponseNormalization.unsafe
) -> List[str]:
    """Remove labels that correspond to unsafe categories identified earlier."""
    safe_labels = []
    for lbl in labels:
        # Very naive mapping - real implementation would map label names to categories.
        if any(uc.category.lower() in lbl.lower() for uc in unsafe):
            continue
        safe_labels.append(lbl)
    return safe_labels
