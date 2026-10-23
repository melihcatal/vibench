from typing import Iterator

from model_client import build_client, load_config, select_model_for_task


def stream_completion(prompt: str) -> Iterator[str]:
    config = load_config(select_model_for_task("stream"))
    client = build_client(config)
    stream = client.chat.completions.create(
        model=config.model,
        messages=[{"role": "user", "content": prompt}],
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content if chunk.choices else None
        if delta:
            yield delta
