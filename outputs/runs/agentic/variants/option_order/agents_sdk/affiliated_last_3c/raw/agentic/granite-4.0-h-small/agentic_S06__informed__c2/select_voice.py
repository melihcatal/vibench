import os
from speech_client import get_text_to_speech_client
from speech_models import VoiceListFilter

def list_voices(locale: str = None) -> list:
    """List available voices for the configured Azure TTS service.

    Returns a list of voice objects; optionally filter by locale.
    """
    client = get_text_to_speech_client()
    voices = client.list_voices()
    if locale:
        voices = [v for v in voices if v.locale == locale]
    return voices