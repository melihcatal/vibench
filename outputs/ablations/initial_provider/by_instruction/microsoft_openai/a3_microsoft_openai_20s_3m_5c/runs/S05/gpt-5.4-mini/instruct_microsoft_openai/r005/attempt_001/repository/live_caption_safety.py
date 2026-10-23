from typing import Iterable, Iterator

from openai import OpenAI

from speech_client import create_openai_client
from speech_models import normalize_transcript


def check_caption_safety(chunks: Iterable[str]) -> Iterator[bool]:
    client = create_openai_client()
    for chunk in chunks:
        text = normalize_transcript(chunk)
        if not text:
            continue
        response = client.moderations.create(model="omni-moderation-latest", input=text)
        yield bool(getattr(response, "results", [{}])[0].get("flagged", False))
