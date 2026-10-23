from __future__ import annotations

from typing import Iterator, Optional

from openai import OpenAI

from model_client import get_client, get_model_name, merge_messages


_PROVIDER = "openai"
_DEFAULT_STREAM_MODEL = "gpt-4o-mini"


def stream_completion(prompt: str, *, client: Optional[OpenAI] = None, model: Optional[str] = None) -> Iterator[str]:
    """Stream partial completion chunks from OpenAI Chat Completions."""
    model_name = model or get_model_name("stream_completion", _DEFAULT_STREAM_MODEL)
    api_client = client or get_client(provider=_PROVIDER)
    messages = merge_messages(system="You are a helpful assistant.", user=prompt)
    stream = api_client.chat.completions.create(
        model=model_name,
        messages=messages,
        stream=True,
        temperature=0.3,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
