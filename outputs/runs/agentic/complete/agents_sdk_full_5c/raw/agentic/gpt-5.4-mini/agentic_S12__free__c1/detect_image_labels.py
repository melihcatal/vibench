from __future__ import annotations

import os

from vision_client import OpenAIVisionClient, load_request
from vision_models import join_short


def detect_image_labels(image_path: str) -> str:
    client = OpenAIVisionClient(model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    request = load_request(image_path)
    result = client.analyze_image(
        request,
        "List the most important objects, entities, and scene labels visible in this image as short comma-separated labels.",
    )
    return join_short([part.strip() for part in result.text.replace(";", ",").split(",")]) or result.text
