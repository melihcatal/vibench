from __future__ import annotations

from typing import Iterator

from model_client import DEFAULT_OPENAI_MODEL, LLMRequest, stream_chat_completion

SYSTEM_PROMPT = "You generate helpful continuations with clean token streaming."


def stream_completion(prompt: str, model: str = DEFAULT_OPENAI_MODEL) -> Iterator[str]:
    request = LLMRequest(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        temperature=0.7,
        max_tokens=400,
    )
    yield from stream_chat_completion(request)
