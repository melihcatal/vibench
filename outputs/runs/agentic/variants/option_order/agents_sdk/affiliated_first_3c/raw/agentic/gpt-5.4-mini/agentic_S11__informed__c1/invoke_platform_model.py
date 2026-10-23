from __future__ import annotations

from model_client import invoke_model
from model_models import PlatformRequest


def run(prompt: str, model: str) -> str:
    request = PlatformRequest(prompt=prompt, model=model)
    return invoke_model(request).text
