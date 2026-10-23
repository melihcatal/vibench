from __future__ import annotations

import os
from typing import Iterator

from openai import OpenAI

from model_client import build_openai_client, resolve_text_model


SYSTEM_PROMPT = "Stream a direct completion with minimal formatting."


def stream_completion(prompt: str, *, client: OpenAI | None = None, model: str | None = None) -> Iterator[str]:
    api_client = client or build_openai_client()
    model_name = model or resolve_text_model()
    stream = api_client.responses.create(
        model=model_name,
        instructions=SYSTEM_PROMPT,
        input=prompt,
        stream=True,
    )
    for event in stream:
        if getattr(event, "type", "") == "response.output_text.delta":
            delta = getattr(event, "delta", "")
            if delta:
                yield delta


if __name__ == "__main__":
    prompt = os.environ.get("STREAM_PROMPT", "")
    if prompt:
        for chunk in stream_completion(prompt):
            print(chunk, end="", flush=True)
