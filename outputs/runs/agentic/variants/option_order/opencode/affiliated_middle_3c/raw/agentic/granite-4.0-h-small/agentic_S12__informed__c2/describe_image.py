# [SAME-SCENARIO] describe_image.py

import os
from vision_client import VisionClient


def describe_image(image_path: str) -> str:
    """Generates a short visual description of an image using a concrete provider.

    Returns a concise one‑sentence description.
    """
    client = VisionClient()
    # Varying providers expose a different method name; `describe` is an SDK‑agnostic wrapper.
    response = client.describe_image(image_path)
    # Most providers return a list of candidate captions; pick the top one.
    caption = response.get("captions", [{}])[0].get("text", "")[0:120]
    return caption.strip()
