from __future__ import annotations

from typing import Iterator

from model_client import get_client, load_config, choose_model

SYSTEM_PROMPT = "You are a helpful assistant that streams concise completions."


def stream_completion(prompt: str) -> Iterator[str]:
    config = load_config()
    client = get_client(config)
    model = choose_model("stream", config)
    stream = client.chat.completions.create(
        model=model,
        temperature=config.temperature,
        stream=True,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
    )
    for chunk in stream:
        delta = getattr(chunk.choices[0].delta, "content", None)
        if delta:
            yield delta
