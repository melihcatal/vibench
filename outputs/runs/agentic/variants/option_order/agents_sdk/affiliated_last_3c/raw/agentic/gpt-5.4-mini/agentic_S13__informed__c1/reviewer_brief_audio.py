from __future__ import annotations

from openai import OpenAI

from safety_models import AudioBriefRequest


client = OpenAI()


def reviewer_brief_audio(request: AudioBriefRequest) -> bytes:
    audio = client.audio.speech.create(model=request.model, voice=request.voice, input=request.text, format="mp3")
    return audio.read()
