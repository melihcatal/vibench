from typing import Iterator

from model_client import load_config, make_client


def stream_completion(prompt: str) -> Iterator[str]:
    config = load_config("stream")
    client = make_client(config)
    stream = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.2,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta
        content = getattr(delta, "content", None)
        if content:
            yield content
