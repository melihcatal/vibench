from typing import Dict

from openai import OpenAI


TTS_MODEL = "gpt-4o-mini-tts"


def localized_audio_preview(text: str, voice: str = "alloy") -> Dict[str, str]:
    client = OpenAI()
    response = client.audio.speech.create(model=TTS_MODEL, voice=voice, input=text)
    return {
        "provider": "openai",
        "model": TTS_MODEL,
        "audio_format": "mp3",
        "status": "created",
    }
