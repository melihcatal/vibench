# [SAME-SCENARIO] score_image_safety.py

import os
from vision_client import VisionClient


def score_image_safety(image_path: str) -> bool:
    """Checks an image for unsafe or policy-sensitive visual content.

    Returns True if the image is deemed safe, False otherwise.
    """
    client = VisionClient()
    # Most providers expose a moderation or safety endpoint; we use the generic `moderation` helper.
    result = client.moderation(image_path)
    # Providers typically return a list of detected categories with confidence scores.
    # Here we deem the image safe if no unsafe category exceeds a threshold.
    unsafe = any(
        entry["category"] in {"adult", "violence", "racy"} and entry["score"] > 0.7
        for entry in result.get("detectedUnsafe", [])
    )
    return not unsafe
