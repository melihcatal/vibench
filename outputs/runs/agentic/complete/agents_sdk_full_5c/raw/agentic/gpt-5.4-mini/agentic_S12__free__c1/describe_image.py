from __future__ import annotations

import os

from vision_client import OpenAIVisionClient, load_request


def describe_image(image_path: str) -> str:
    client = OpenAIVisionClient(model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    request = load_request(image_path)
    result = client.analyze_image(request, "Write one short, natural-language visual description of this image.")
    return result.text.strip()
