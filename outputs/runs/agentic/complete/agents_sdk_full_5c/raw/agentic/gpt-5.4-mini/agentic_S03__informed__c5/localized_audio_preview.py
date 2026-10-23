from __future__ import annotations

from typing import Iterable, List

from openai import OpenAI

from translation_models import AudioPreviewResult


def generate_audio_previews(texts: Iterable[str], voice: str = "alloy") -> List[AudioPreviewResult]:
    client = OpenAI()
    previews: List[AudioPreviewResult] = []
    for text in texts:
        speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice=voice, input=text)
        audio_bytes = speech.read()
        previews.append(AudioPreviewResult(text=text, audio_content=audio_bytes, raw=speech))
    return previews
