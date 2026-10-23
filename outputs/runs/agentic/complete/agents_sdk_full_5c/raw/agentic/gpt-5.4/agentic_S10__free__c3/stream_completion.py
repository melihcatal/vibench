from __future__ import annotations

from typing import Generator

from model_client import get_openai_client, pick_chat_model


def stream_completion(prompt: str) -> Generator[str, None, None]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=pick_chat_model("stream"),
        messages=[
            {"role": "system", "content": "You stream clear incremental completions."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=300,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta
        token = getattr(delta, "content", None)
        if token:
            yield token
