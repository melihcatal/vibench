from __future__ import annotations

from typing import Optional

from openai import OpenAI

AUDIO_MODEL = "gpt-4o-mini-tts"
VOICE = "alloy"


def generate_reviewer_brief_audio(text: str, out_path: Optional[str] = None) -> bytes:
    client = OpenAI()
    result = client.audio.speech.create(model=AUDIO_MODEL, voice=VOICE, input=text)
    audio_bytes = result.read()
    if out_path:
        with open(out_path, "wb") as f:
            f.write(audio_bytes)
    return audio_bytes
