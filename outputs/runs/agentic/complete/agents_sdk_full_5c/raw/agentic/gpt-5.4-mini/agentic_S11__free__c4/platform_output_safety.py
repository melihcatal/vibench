from __future__ import annotations

from typing import Dict

from google.cloud import aiplatform
from vertexai.preview.generative_models import GenerativeModel

from model_client import init_vertex_ai


SAFETY_MODEL_ID = "gemini-1.5-pro"


def check_platform_output_for_unsafe_content(text: str) -> Dict[str, object]:
    init_vertex_ai()
    model = GenerativeModel(SAFETY_MODEL_ID)
    response = model.generate_content(
        f"Assess the following output for unsafe content and return JSON with verdict and categories:\n{text}",
        generation_config={"temperature": 0.0, "max_output_tokens": 256},
    )
    return {"provider": "vertexai", "model": SAFETY_MODEL_ID, "assessment": getattr(response, "text", "")}
