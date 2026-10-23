from __future__ import annotations

from typing import Iterator, Optional

from openai import OpenAI

from model_client import build_client, model_for_task
from model_models import ChatRequest


OPENAI_STREAM_MODEL = "gpt-4o-mini"


def stream_completion(prompt: str, client: Optional[OpenAI] = None) -> Iterator[str]:
    client = client or build_client()
    request = ChatRequest(
        task="stream_completion",
        model=model_for_task("stream_completion", default=OPENAI_STREAM_MODEL),
        system_prompt="You produce useful streaming completions.",
        user_prompt=prompt,
    )
    stream = client.chat.completions.create(
        model=request.model,
        messages=request.messages(),
        temperature=0.3,
        stream=True,
    )
    for chunk in stream:
        delta = chunk.choices[0].delta.content
        if delta:
            yield delta
