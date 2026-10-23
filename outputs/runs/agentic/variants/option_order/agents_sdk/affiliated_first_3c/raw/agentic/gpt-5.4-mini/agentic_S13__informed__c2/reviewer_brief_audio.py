from __future__ import annotations

from typing import Optional

from openai import OpenAI


def reviewer_brief_audio(text: str) -> bytes:
    client = OpenAI()
    speech = client.audio.speech.create(model="gpt-4o-mini-tts", voice="alloy", input=text)
    return speech.read()
