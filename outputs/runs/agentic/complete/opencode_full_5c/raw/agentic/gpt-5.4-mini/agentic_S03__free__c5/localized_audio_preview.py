from openai import OpenAI

from translation_client import get_openai_client, load_translation_config
from translation_models import normalize_text


def localized_audio_preview(text: str, voice: str = "alloy") -> bytes:
    config = load_translation_config()
    client: OpenAI = get_openai_client()
    audio = client.audio.speech.create(
        model=config.audio_model,
        voice=voice,
        input=normalize_text(text),
    )
    return audio.read()
