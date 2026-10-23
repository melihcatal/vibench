from typing import Optional

from model_client import get_client, resolve_model_name
from model_models import normalize_text


def platform_brief_audio(text: str, voice: str = "alloy", model: Optional[str] = None) -> bytes:
    client = get_client()
    model_name = resolve_model_name(model)
    speech = client.audio.speech.create(
        model=model_name,
        voice=voice,
        input=normalize_text(text),
        format="mp3",
    )
    return speech.read()
