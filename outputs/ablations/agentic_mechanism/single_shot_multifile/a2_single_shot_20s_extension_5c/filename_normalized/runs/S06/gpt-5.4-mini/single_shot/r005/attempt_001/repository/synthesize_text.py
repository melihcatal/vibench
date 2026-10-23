from __future__ import annotations

from speech_client import get_tts_client, resolve_audio_format
from speech_models import TextToSpeechRequest, TextToSpeechResponse, normalize_text


def synthesize_text(text: str, voice_name: str | None = None, locale: str | None = None, audio_format: str = "MP3") -> TextToSpeechResponse:
    client = get_tts_client()
    normalized_text = normalize_text(text)
    fmt = resolve_audio_format(audio_format)
    request = TextToSpeechRequest(text=normalized_text, voice_name=voice_name, locale=locale, audio_format=fmt)
    return client.synthesize_text(request)
