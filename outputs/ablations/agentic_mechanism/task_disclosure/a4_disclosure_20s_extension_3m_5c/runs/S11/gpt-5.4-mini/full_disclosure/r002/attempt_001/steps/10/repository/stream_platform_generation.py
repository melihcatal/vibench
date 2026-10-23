from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, Iterable, Iterator, List, Optional

try:
    from openai import OpenAI
except Exception as exc:  # pragma: no cover
    raise RuntimeError("openai package is required") from exc


@dataclass
class StreamedPlatformChunk:
    text: str
    raw: Any


def _extract_text(delta: Any) -> str:
    if delta is None:
        return ""
    if isinstance(delta, str):
        return delta
    text = getattr(delta, "text", None)
    if isinstance(text, str):
        return text
    content = getattr(delta, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(delta, dict):
        for key in ("text", "content"):
            value = delta.get(key)
            if isinstance(value, str):
                return value
        choices = delta.get("choices")
        if isinstance(choices, list) and choices:
            return _extract_text(choices[0].get("delta") if isinstance(choices[0], dict) else None)
    return ""


def stream_platform_generation(
    messages: List[Dict[str, str]],
    *,
    model: str = "gpt-4.1-mini",
    base_url: Optional[str] = None,
    api_key: Optional[str] = None,
    **kwargs: Any,
) -> Iterator[StreamedPlatformChunk]:
    client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"), base_url=base_url)
    stream = client.responses.stream(model=model, input=messages, **kwargs)
    with stream as response_stream:
        for event in response_stream:
            text = _extract_text(getattr(event, "delta", None))
            if not text and isinstance(event, dict):
                text = _extract_text(event)
            yield StreamedPlatformChunk(text=text, raw=event)


def collect_stream_text(chunks: Iterable[StreamedPlatformChunk]) -> str:
    return "".join(chunk.text for chunk in chunks)
