import os
from vision_client import VisionClient
import json


def check_generated_labels_for_unsafe_text(labels: list) -> list:
    """Quick safety filter for label strings.

    Args:
        labels: List of label strings produced by visual analysis.

    Returns:
        Filtered list containing only safe labels.
    """
    # Placeholder: replace with real moderation API if necessary
    unsafe_terms = {"violence", "adult", "racy", "medical"}
    safe_labels = [
        lbl for lbl in labels if not unsafe_terms.intersection(lbl.lower().split())
    ]
    return safe_labels


def audit_generated_description(description: str) -> bool:
    """Check if description contains disallowed content using a simple rule set.

    Args:
        description: Generated description text.

    Returns:
        True if safe, False if unsafe.
    """
    unsafe_phrases = ["explicit content", "adult activity", "violent act"]
    return not any(phrase in description.lower() for phrase in unsafe_phrases)
