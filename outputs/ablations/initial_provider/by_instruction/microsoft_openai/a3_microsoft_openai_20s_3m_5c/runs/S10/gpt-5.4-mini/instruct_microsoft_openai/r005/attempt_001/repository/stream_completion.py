from typing import Iterator

from model_client import get_client, get_model


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_client()
    stream = client.chat.completions.create(
        model=get_model(),
        stream=True,
        messages=[{"role": "user", "content": prompt}],
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
