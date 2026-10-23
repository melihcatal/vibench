from __future__ import annotations

from speech_client import get_tts_client, resolve_audio_format
from speech_models import SsmlRequest, TextToSpeechResponse, normalize_ssml


def synthesize_ssml(ssml: str, voice_name: str | None = None, locale: str | None = None, audio_format: str = "MP3") -> TextToSpeechResponse:
    client = get_tts_client()
    normalized_ssml = normalize_ssml(ssml)
    fmt = resolve_audio_format(audio_format)
    request = SsmlRequest(ssml=normalized_ssml, voice_name=voice_name, locale=locale, audio_format=fmt)
    return client.synthesize_ssml(request)
