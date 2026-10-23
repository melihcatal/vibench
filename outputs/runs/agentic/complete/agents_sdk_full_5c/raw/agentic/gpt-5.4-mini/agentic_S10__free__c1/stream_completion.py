from __future__ import annotations

from typing import Iterator

from model_client import get_model_name, get_openai_client

PROVIDER = "openai"
MODEL_FAMILY = "gpt-4o"


def stream_completion(prompt: str, model: str | None = None) -> Iterator[str]:
    client = get_openai_client()
    stream = client.responses.create(
        model=get_model_name(model),
        input=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for event in stream:
        if getattr(event, "type", None) == "response.output_text.delta":
            delta = getattr(event, "delta", "")
            if delta:
                yield delta
