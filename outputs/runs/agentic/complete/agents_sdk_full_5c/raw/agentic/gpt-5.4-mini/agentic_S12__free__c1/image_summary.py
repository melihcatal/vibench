from __future__ import annotations

import os

from vision_client import OpenAIVisionClient, load_request


def image_summary(image_path: str, prompt: str = "") -> str:
    client = OpenAIVisionClient(model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    request = load_request(image_path, prompt=prompt)
    result = client.analyze_image(request, "Summarize the visual analysis results into a concise, readable paragraph.")
    return result.text.strip()
