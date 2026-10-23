from model_client import get_xai_client
from model_models import normalize_stream_chunk
from typing import Iterator


def stream_completion(prompt: str) -> Iterator[str]:
    client = get_xai_client()
    stream = client.chat.completions.create(
        model="grok-beta",
        messages=[{"role": "user", "content": prompt}],
        stream=True,
        temperature=0.7,
    )
    for chunk in stream:
        yield normalize_stream_chunk(chunk)
