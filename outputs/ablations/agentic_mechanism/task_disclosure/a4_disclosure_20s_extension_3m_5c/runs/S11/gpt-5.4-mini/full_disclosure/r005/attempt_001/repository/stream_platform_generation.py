import os
from typing import Iterator, Any, Dict

from openai import OpenAI


def stream_platform_generation(prompt: str, model: str | None = None) -> Iterator[Dict[str, Any]]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    stream = client.responses.create(
        model=model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt,
        stream=True,
    )
    for event in stream:
        yield {"provider": "openai", "event": event}
