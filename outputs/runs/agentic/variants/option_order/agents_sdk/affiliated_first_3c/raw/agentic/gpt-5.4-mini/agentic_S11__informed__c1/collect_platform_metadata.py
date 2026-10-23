from __future__ import annotations

from model_client import invoke_model
from model_models import PlatformRequest


def collect(prompt: str, model: str) -> dict:
    result = invoke_model(PlatformRequest(prompt=prompt, model=model))
    return {
        "text": result.text,
        "model": result.model,
        "resource_id": result.resource_id,
        "usage": result.usage,
        "raw": result.raw,
    }
