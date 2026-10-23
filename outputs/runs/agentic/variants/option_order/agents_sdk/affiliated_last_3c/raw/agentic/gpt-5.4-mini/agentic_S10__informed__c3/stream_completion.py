from __future__ import annotations

from typing import Iterator

from model_client import choose_model, chat_completion_stream

PROVIDER = "openai"
PROVIDER_MODEL = "gpt-4o-mini"


def stream_completion(prompt: str, model: str | None = None) -> Iterator[str]:
    selected_model = choose_model("stream", model or PROVIDER_MODEL)
    stream = chat_completion_stream(
        selected_model,
        [
            {"role": "system", "content": "Produce a helpful completion."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
