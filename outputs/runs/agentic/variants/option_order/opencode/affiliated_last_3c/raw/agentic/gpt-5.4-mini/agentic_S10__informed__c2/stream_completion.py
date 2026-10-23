from typing import Iterator

from model_client import get_client, get_model_family, normalize_text


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_client()
    stream = client.chat.completions.create(
        model=get_model_family("gpt-4.1-mini"),
        messages=[{"role": "user", "content": normalize_text(prompt)}],
        stream=True,
    )
    for event in stream:
        delta = event.choices[0].delta.content if event.choices else None
        if delta:
            yield delta
