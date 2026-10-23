import os
from typing import Iterable, Iterator, List, Optional

from openai import OpenAI


def _chunk_text_from_event(event) -> str:
    delta = getattr(event, "delta", None)
    if delta is None:
        return ""
    content = getattr(delta, "content", None)
    if content is None:
        return ""
    if isinstance(content, list):
        parts: List[str] = []
        for item in content:
            text = getattr(item, "text", None)
            if text is not None:
                parts.append(text)
        return "".join(parts)
    if isinstance(content, str):
        return content
    return ""


def stream_platform_generation(
    prompt: str,
    model: str = "gpt-4o-mini",
    system: Optional[str] = None,
) -> Iterator[object]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    with client.responses.stream(model=model, input=messages) as stream:
        for event in stream:
            text = _chunk_text_from_event(event)
            if text:
                yield text
            yield event


def collect_stream(prompt: str, model: str = "gpt-4o-mini", system: Optional[str] = None) -> List[object]:
    return list(stream_platform_generation(prompt=prompt, model=model, system=system))
