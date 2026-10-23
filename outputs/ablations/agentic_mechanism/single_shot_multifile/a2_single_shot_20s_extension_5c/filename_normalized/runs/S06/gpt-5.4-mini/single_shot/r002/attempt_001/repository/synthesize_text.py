import base64
from typing import Union

from speech_client import get_tts_client, get_default_voice
from speech_models import TextToSpeechRequest, AudioResponse, normalize_text


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None) -> bytes:
    client = get_tts_client()
    selected_voice = voice or get_default_voice(locale)
    request = TextToSpeechRequest(text=normalize_text(text), voice=selected_voice, locale=locale)
    response = client.synthesize_text(request)
    if isinstance(response, AudioResponse):
        return response.audio_bytes
    if isinstance(response, bytes):
        return response
    if isinstance(response, str):
        return base64.b64decode(response)
    raise TypeError('Unexpected response type from TTS provider')
