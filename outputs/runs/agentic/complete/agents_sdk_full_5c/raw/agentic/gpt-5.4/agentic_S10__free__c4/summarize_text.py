from __future__ import annotations

from model_client import HostedModelClient
from model_models import NormalizedTextResult


def summarize_text(text: str, max_tokens: int = 220) -> NormalizedTextResult:
    client = HostedModelClient()
    request = client.build_request(
        task="summarization",
        system_prompt="You are a precise summarization assistant. Produce a concise summary with key facts retained.",
        user_prompt=f"Summarize the following text:\n\n{text}",
        temperature=0.2,
        max_tokens=max_tokens,
    )
    return client.generate(request)
