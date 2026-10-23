from typing import Iterable, Iterator

from openai import OpenAI

from speech_client import create_openai_client
from speech_models import normalize_transcript


def translate_live_captions(chunks: Iterable[str], target_language: str) -> Iterator[str]:
    client = create_openai_client()
    for chunk in chunks:
        text = normalize_transcript(chunk)
        if not text:
            continue
        response = client.responses.create(model="gpt-4o-mini", input=f"Translate to {target_language}: {text}")
        yield getattr(response, "output_text", "")
