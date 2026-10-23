from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import DEFAULT_TTS_VOICE, get_openai_client, pick_model


def spoken_brief(text: str, output_path: str, voice: Optional[str] = None, model: str = "gpt-4o-mini-tts") -> str:
    client: OpenAI = get_openai_client()
    chosen_voice = voice or DEFAULT_TTS_VOICE
    with client.audio.speech.with_streaming_response.create(
        model=pick_model(model, family="tts"),
        voice=chosen_voice,
        input=text,
        format="mp3",
    ) as response:
        response.stream_to_file(output_path)
    return output_path
