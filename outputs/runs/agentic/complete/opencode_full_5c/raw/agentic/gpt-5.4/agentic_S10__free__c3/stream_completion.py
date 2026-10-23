from __future__ import annotations

from typing import Iterator

from model_client import DEFAULT_CHAT_MODEL, get_openai_client, iter_stream_text


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_openai_client()
    stream = client.responses.stream(
        model=DEFAULT_CHAT_MODEL,
        input=[
            {
                "role": "system",
                "content": "Complete the user's prompt helpfully and clearly.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
    )
    with stream as events:
        for chunk in iter_stream_text(events):
            yield chunk
