from openai import OpenAI

from translation_client import get_client, get_model_name
from translation_models import normalize_text


def localized_audio_preview(text: str, voice: str = "alloy") -> bytes:
    client: OpenAI = get_client()
    result = client.audio.speech.create(
        model="gpt-4o-mini-tts", voice=normalize_text(voice), input=normalize_text(text)
    )
    return result.read()
