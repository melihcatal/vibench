import os
from typing import Iterable, Iterator, Optional

from openai import OpenAI


def stream_completion(
    prompt: str,
    model: str = "gpt-5.4-mini",
    system: Optional[str] = None,
) -> Iterator[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})

    stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    for chunk in stream:
        for choice in getattr(chunk, "choices", []):
            delta = getattr(choice, "delta", None)
            content = getattr(delta, "content", None) if delta is not None else None
            if content:
                yield content
