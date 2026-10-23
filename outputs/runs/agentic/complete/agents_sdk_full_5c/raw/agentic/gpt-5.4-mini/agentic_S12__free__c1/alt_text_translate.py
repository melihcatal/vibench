from __future__ import annotations

import os

from vision_client import OpenAIVisionClient
from vision_models import VisualRequest


def alt_text_translate(image_path: str, language: str = "Spanish") -> str:
    client = OpenAIVisionClient(model=os.getenv("OPENAI_VISION_MODEL", "gpt-4o-mini"))
    request = VisualRequest(image_path=image_path, language=language)
    result = client.analyze_image(request, f"Translate the generated image alt text into {language}. Return only the translation.")
    return result.text.strip()
