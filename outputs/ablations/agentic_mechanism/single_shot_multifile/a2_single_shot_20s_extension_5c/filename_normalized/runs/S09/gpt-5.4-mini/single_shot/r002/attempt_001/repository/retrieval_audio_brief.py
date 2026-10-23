import os
from typing import List

from openai import OpenAI

from embeddings_models import normalize_texts


AUDIO_MODEL = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")


def generate_spoken_brief(results: List[str], api_key: str | None = None) -> bytes:
    client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))
    text = "Brief search results:\n" + "\n".join(normalize_texts(results))
    speech = client.audio.speech.create(model=AUDIO_MODEL, voice=os.getenv("OPENAI_TTS_VOICE", "alloy"), input=text)
    return speech.read()
