import os
from openai import OpenAI

_PROVIDER_TEXT_MODEL = os.getenv("OPENAI_AUDIO_TEXT_MODEL", "gpt-4o-mini")
_PROVIDER_AUDIO_MODEL = os.getenv("OPENAI_AUDIO_MODEL", "tts-1")


def localized_audio_preview(text: str, voice: str = "alloy") -> bytes:
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY")) if os.getenv("OPENAI_API_KEY") else OpenAI()
    response = client.audio.speech.create(model=_PROVIDER_AUDIO_MODEL, voice=voice, input=text)
    return response.read()
