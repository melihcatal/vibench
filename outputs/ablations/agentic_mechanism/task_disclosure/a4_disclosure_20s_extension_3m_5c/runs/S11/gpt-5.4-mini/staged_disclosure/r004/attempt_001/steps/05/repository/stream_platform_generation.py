import os
from typing import Iterator, Optional

from openai import OpenAI


def stream_platform_generation(
    prompt: str,
    model: str = "gpt-4.1-mini",
    system: Optional[str] = None,
) -> Iterator[object]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = []
    if system:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    stream = client.chat.completions.create(model=model, messages=messages, stream=True)
    for chunk in stream:
        yield chunk


def generate_text(prompt: str, model: str = "gpt-4.1-mini", system: Optional[str] = None) -> str:
    text_parts = []
    for chunk in stream_platform_generation(prompt=prompt, model=model, system=system):
        if getattr(chunk, "choices", None):
            delta = chunk.choices[0].delta
            content = getattr(delta, "content", None)
            if content:
                text_parts.append(content)
    return "".join(text_parts)
