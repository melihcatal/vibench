from __future__ import annotations

from collections.abc import Iterator

from model_client import client_for, load_config

SYSTEM_PROMPT = "Continue the user's text with useful, coherent completion."


def stream_completion(prompt: str, model: str | None = None) -> Iterator[str]:
    cfg = load_config(model)
    client = client_for(cfg)
    stream = client.chat.completions.create(
        model=cfg.model,
        messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
        stream=True,
    )
    for event in stream:
        for choice in getattr(event, "choices", []):
            delta = getattr(choice, "delta", None)
            text = getattr(delta, "content", None) if delta is not None else None
            if text:
                yield text
