from __future__ import annotations

from collections.abc import Iterator

from openai import OpenAI

from model_client import choose_model, get_openai_client, normalize_messages


def stream_completion(prompt: str, model: str | None = None) -> Iterator[str]:
    client: OpenAI = get_openai_client()
    stream = client.chat.completions.create(
        model=choose_model(model, family="chat"),
        messages=normalize_messages("Stream a helpful completion.", prompt),
        temperature=0.3,
        stream=True,
    )
    for event in stream:
        delta = getattr(event.choices[0].delta, "content", None)
        if delta:
            yield delta
