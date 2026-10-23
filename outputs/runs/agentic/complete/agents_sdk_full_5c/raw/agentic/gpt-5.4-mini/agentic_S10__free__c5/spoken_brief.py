from openai import OpenAI

from model_client import get_client, select_audio_model


PROVIDER = "openai"
DEFAULT_MODEL = "gpt-4o-mini-tts"


def spoken_brief(text: str, voice: str = "alloy"):
    client = get_client()
    model = select_audio_model(default=DEFAULT_MODEL)
    return client.audio.speech.create(model=model, voice=voice, input=text)
