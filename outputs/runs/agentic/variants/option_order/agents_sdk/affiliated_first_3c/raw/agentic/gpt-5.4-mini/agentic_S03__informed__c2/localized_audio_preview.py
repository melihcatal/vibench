from __future__ import annotations

import os

from openai import OpenAI


def localized_audio_preview(translated_copy: str) -> str:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice="alloy",
        input=translated_copy,
        format="mp3",
    )
    return response.content.decode("latin1") if hasattr(response, "content") else ""
