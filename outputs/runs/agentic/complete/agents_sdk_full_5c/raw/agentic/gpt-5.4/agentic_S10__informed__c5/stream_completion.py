from __future__ import annotations

from typing import Iterable

from model_client import stream_text
from model_models import InferenceRequest


def stream_completion(prompt: str, model: str | None = None) -> Iterable[str]:
    request = InferenceRequest(
        system_prompt="You are a helpful streaming assistant.",
        user_prompt=prompt,
        temperature=0.4,
        max_tokens=350,
        model=model,
    )
    return stream_text(request)
