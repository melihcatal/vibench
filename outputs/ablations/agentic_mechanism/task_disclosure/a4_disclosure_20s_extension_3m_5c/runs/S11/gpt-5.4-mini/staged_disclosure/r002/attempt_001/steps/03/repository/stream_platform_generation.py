import os
from typing import Any, Dict, Iterator, Optional

from openai import OpenAI


def stream_platform_generation(
    prompt: str,
    model: str = "gpt-4.1-mini",
    system: Optional[str] = None,
    temperature: float = 0.7,
) -> Iterator[Dict[str, Any]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    messages = []
    if system is not None:
        messages.append({"role": "system", "content": system})
    messages.append({"role": "user", "content": prompt})
    with client.responses.stream(model=model, input=messages, temperature=temperature) as stream:
        for event in stream:
            yield {
                "event": event,
                "response": getattr(event, "response", None),
                "type": getattr(event, "type", None),
            }


def collect_stream_text(prompt: str, model: str = "gpt-4.1-mini") -> str:
    chunks = []
    for item in stream_platform_generation(prompt=prompt, model=model):
        event = item["event"]
        if getattr(event, "type", None) == "response.output_text.delta":
            delta = getattr(event, "delta", None)
            if delta:
                chunks.append(delta)
    return "".join(chunks)


__all__ = ["stream_platform_generation", "collect_stream_text"]
