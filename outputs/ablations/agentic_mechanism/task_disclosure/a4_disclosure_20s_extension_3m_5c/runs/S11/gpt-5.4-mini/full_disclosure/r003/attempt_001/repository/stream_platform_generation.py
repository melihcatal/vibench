from __future__ import annotations

import os
from typing import Any, Dict, Iterable, Iterator, Optional, Tuple

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))


def stream_platform_generation(
    prompt: str,
    *,
    model: str = "gpt-5.4-mini",
    system: Optional[str] = None,
    extra: Optional[Dict[str, Any]] = None,
) -> Iterator[Tuple[Any, Any]]:
    client = _client()
    messages = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    stream = client.responses.stream(model=model, input=messages, **(extra or {}))
    with stream as response_stream:
        for event in response_stream:
            yield event, response_stream


def collect_stream_text(prompt: str, *, model: str = "gpt-5.4-mini") -> str:
    chunks = []
    for event, _response in stream_platform_generation(prompt, model=model):
        text = getattr(event, "delta", None)
        if isinstance(text, str):
            chunks.append(text)
        else:
            item = getattr(event, "output_text", None)
            if isinstance(item, str):
                chunks.append(item)
    return "".join(chunks)
