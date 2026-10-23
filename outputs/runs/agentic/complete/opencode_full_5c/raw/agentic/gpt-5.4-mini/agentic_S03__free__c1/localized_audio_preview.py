from openai import OpenAI

from translation_client import get_client


TTS_MODEL = "gpt-4o-mini-tts"


def localized_audio_preview(text: str, voice: str = "alloy"):
    client: OpenAI = get_client()
    response = client.audio.speech.create(model=TTS_MODEL, voice=voice, input=text)
    return response
