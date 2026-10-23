from typing import Dict

from openai import OpenAI

from safety_client import load_safety_config


def reviewer_brief_audio(text: str, voice: str = "alloy") -> Dict[str, str]:
    config = load_safety_config()
    client = OpenAI(api_key=config.openai_api_key)
    response = client.audio.speech.create(
        model="gpt-4o-mini-tts",
        voice=voice,
        input=text,
    )
    return {"provider": "openai", "model": "gpt-4o-mini-tts", "voice": voice, "audio_format": "mp3"}