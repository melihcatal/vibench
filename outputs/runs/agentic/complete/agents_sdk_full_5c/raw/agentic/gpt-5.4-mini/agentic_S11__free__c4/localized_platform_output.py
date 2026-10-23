from __future__ import annotations

from typing import Dict

from vertexai.generative_models import GenerativeModel

from model_client import init_vertex_ai


TRANSLATION_MODEL_ID = "gemini-1.5-pro"


def localize_platform_output(text: str, target_locale: str = "es") -> Dict[str, str]:
    init_vertex_ai()
    model = GenerativeModel(TRANSLATION_MODEL_ID)
    response = model.generate_content(f"Translate the following text into {target_locale}:\n{text}")
    return {"provider": "vertexai", "model": TRANSLATION_MODEL_ID, "locale": target_locale, "text": getattr(response, "text", "")}
