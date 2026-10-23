from __future__ import annotations

from typing import Iterator

from openai import OpenAI

from model_client import LLMConfig, get_openai_client
from model_models import StreamingChunk

STREAM_MODEL = "gpt-4.1-mini"


def stream_completion(prompt: str, client: OpenAI | None = None) -> Iterator[StreamingChunk]:
    cfg = LLMConfig(chat_model=STREAM_MODEL)
    llm = client or get_openai_client(cfg)
    stream = llm.chat.completions.create(
        model=cfg.chat_model,
        messages=[
            {"role": "system", "content": "Stream a helpful completion."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        stream=True,
    )
    for event in stream:
        delta = getattr(event.choices[0].delta, "content", None) or ""
        yield StreamingChunk(delta=delta, finished=False)
    yield StreamingChunk(delta="", finished=True)
