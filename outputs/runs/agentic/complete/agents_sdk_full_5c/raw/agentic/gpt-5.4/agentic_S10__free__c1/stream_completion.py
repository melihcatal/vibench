from __future__ import annotations

from typing import Iterator

from model_client import choose_model, get_openai_client
from model_models import ChatMessage, messages_to_dicts


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=choose_model("stream"),
        messages=messages_to_dicts(
            [
                ChatMessage(role="system", content="Respond helpfully and stream tokens as they are generated."),
                ChatMessage(role="user", content=prompt),
            ]
        ),
        temperature=0.3,
        stream=True,
    )
    for chunk in stream:
        if not chunk.choices:
            continue
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
