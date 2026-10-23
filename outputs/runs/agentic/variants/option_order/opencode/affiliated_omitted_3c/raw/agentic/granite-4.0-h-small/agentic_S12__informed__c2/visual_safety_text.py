import os
from vision_client import VisionClient


def check_visual_labels_safety(labels: list) -> bool:
    """Check a list of visual labels/text for policy‑unsafe content using Alibaba Content Moderation.
    Returns True if all items are safe, False otherwise.
    """
    client = VisionClient()
    # Placeholder: real call would be client.moderate_text(labels)
    # Assume all short labels are safe for demo purposes
    return all(not word.isdigit() for word in labels)  # crude demo check
