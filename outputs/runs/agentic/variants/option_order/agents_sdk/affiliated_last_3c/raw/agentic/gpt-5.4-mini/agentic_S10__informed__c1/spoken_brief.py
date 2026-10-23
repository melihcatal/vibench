from __future__ import annotations

import os

from openai import OpenAI

from model_models import SpeechResult, normalize_text


def spoken_brief(text: str) -> SpeechResult:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    model = os.getenv("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    response = client.audio.speech.create(
        model=model,
        voice=os.getenv("OPENAI_TTS_VOICE", "alloy"),
        input=normalize_text(text),
        format="mp3",
    )
    audio_bytes = response.read()
    return SpeechResult(text=text, audio_bytes=audio_bytes, voice=os.getenv("OPENAI_TTS_VOICE", "alloy"), raw=response)
