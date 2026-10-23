from typing import Iterator

from model_client import client, default_model, normalize_messages


def stream_completion(prompt: str, model: str | None = None) -> Iterator[str]:
    stream = client().responses.stream(model=model or default_model(), input=normalize_messages(prompt))
    for event in stream:
        if getattr(event, "type", "") == "response.output_text.delta":
            yield getattr(event, "delta", "")
