from typing import Iterator

from model_client import get_client, pick_model


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_client()
    model = pick_model("answer")
    stream = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
