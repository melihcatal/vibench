import os
from typing import Iterable, Optional

from openai import OpenAI


def stream_completion(prompt: str, model: Optional[str] = None) -> Iterable[str]:
    client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
    chosen_model = model or os.environ.get("OPENAI_MODEL", "gpt-4o-mini")
    stream = client.chat.completions.create(
        model=chosen_model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for event in stream:
        for choice in getattr(event, "choices", []):
            delta = getattr(choice, "delta", None)
            content = getattr(delta, "content", None) if delta is not None else None
            if content:
                yield content
