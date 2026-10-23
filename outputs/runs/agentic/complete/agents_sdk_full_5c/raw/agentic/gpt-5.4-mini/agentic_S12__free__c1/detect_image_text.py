from __future__ import annotations

import os

from vision_client import OpenAIVisionClient, load_request


def detect_image_text(image_path: str) -> str:
    client = OpenAIVisionClient(model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    request = load_request(image_path)
    result = client.analyze_image(request, "Extract any visible text in the image. Preserve line breaks when useful and return only the text.")
    return result.text.strip()
