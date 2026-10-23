import os
from typing import Any

from openai import OpenAI

from safety_client import get_openai_client, normalize_text_input


def reviewer_brief_audio(text: Any) -> bytes:
    client: OpenAI = get_openai_client()
    response = client.audio.speech.create(
        model=os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts"),
        voice=os.environ.get("OPENAI_TTS_VOICE", "alloy"),
        input=normalize_text_input(text),
    )
    return response.read()
