from __future__ import annotations

from model_client import DEFAULT_TTS_MODEL, DEFAULT_TTS_VOICE, get_openai_client


def generate_spoken_brief(
    text: str, instructions: str = "Speak clearly and professionally."
) -> bytes:
    client = get_openai_client()
    response = client.audio.speech.create(
        model=DEFAULT_TTS_MODEL,
        voice=DEFAULT_TTS_VOICE,
        input=text,
        instructions=instructions,
        format="mp3",
    )
    return response.read()
