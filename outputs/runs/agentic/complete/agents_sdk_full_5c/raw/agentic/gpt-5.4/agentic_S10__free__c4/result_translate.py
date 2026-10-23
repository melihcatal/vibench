from __future__ import annotations

from model_client import HostedModelClient
from model_models import NormalizedTextResult


def result_translate(text: str, target_language: str) -> NormalizedTextResult:
    client = HostedModelClient()
    request = client.build_request(
        task="translation",
        system_prompt="You are a professional translator. Preserve meaning, names, and formatting where practical.",
        user_prompt=f"Translate the following text into {target_language}:\n\n{text}",
        temperature=0.2,
        max_tokens=500,
    )
    return client.generate(request)
