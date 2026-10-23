import os
from typing import Iterator, Optional

from openai import OpenAI


def stream_completion(prompt: str, model: Optional[str] = None) -> Iterator[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    model_name = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    stream = client.chat.completions.create(
        model=model_name,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        for choice in chunk.choices:
            content = choice.delta.content
            if content:
                yield content
