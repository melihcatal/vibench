from typing import Iterator

from model_client import get_openai_client, model_name
from model_models import normalize_text


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_openai_client()
    stream = client.chat.completions.create(
        model=model_name("stream"),
        messages=[{"role": "user", "content": normalize_text(prompt)}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
