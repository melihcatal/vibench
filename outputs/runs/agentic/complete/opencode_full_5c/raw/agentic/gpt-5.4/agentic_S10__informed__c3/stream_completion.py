from __future__ import annotations

from typing import Iterator

from model_client import default_config, stream_text
from model_models import ChatTurn, LLMRequest


def stream_completion(prompt: str) -> Iterator[str]:
    request = LLMRequest(
        system="You are a helpful assistant generating incremental output.",
        messages=[ChatTurn(role="user", content=prompt)],
        config=default_config("stream", max_output_tokens=500, temperature=0.3),
    )
    return stream_text(request)
