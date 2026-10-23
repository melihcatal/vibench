from __future__ import annotations

from typing import Iterator

from model_client import get_openai_client


def stream_completion(prompt: str, model: str = "gpt-4.1-mini") -> Iterator[str]:
    client = get_openai_client()
    with client.responses.stream(
        model=model,
        input=[
            {"role": "system", "content": "You produce helpful streamed completions."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_output_tokens=500,
    ) as stream:
        for event in stream:
            if event.type == "response.output_text.delta":
                yield event.delta
