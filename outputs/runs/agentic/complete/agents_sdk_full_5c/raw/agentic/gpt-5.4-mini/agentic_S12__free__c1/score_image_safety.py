from __future__ import annotations

import os

from vision_client import OpenAIVisionClient, load_request


def score_image_safety(image_path: str) -> str:
    client = OpenAIVisionClient(model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    request = load_request(image_path)
    result = client.safety_score(request)
    return result.text.strip()
