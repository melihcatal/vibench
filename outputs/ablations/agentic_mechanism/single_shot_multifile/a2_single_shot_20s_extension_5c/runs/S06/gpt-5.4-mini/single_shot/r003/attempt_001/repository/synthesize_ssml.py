from __future__ import annotations

from typing import Optional

from speech_client import get_tts_client, resolve_voice, voice_name_for_locale
from speech_models import SynthesisRequest, SynthesisResult, normalize_ssml


def synthesize_ssml(ssml: str, locale: str = "en-US", voice: Optional[str] = None, rate: str = "0%", pitch: str = "0%", audio_format: str = "mp3") -> SynthesisResult:
    client = get_tts_client()
    selected_voice = voice or voice_name_for_locale(locale)
    normalized_ssml = normalize_ssml(ssml)
    request = SynthesisRequest(text=normalized_ssml, voice=resolve_voice(selected_voice, locale), audio_format=audio_format, is_ssml=True, rate=rate, pitch=pitch)
    response = client.synthesize(request)
    return SynthesisResult(audio_bytes=response.audio_bytes, content_type=response.content_type, voice=response.voice, text=normalized_ssml)
