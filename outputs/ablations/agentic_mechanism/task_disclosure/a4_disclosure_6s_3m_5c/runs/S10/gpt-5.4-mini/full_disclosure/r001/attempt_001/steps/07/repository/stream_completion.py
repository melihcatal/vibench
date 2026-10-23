import os
from typing import Iterator, Optional

from openai import OpenAI


def stream_completion(prompt: str, model: Optional[str] = None) -> Iterator[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    response = client.responses.stream(
        model=model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini"),
        input=prompt,
    )
    with response as stream:
        for event in stream:
            if getattr(event, "type", None) == "response.output_text.delta":
                delta = getattr(event, "delta", None)
                if delta:
                    yield delta
