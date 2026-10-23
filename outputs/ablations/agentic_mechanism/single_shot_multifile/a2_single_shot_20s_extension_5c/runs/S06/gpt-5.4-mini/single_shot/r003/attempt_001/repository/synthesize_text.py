from __future__ import annotations

import base64
from typing import Optional

from speech_client import get_tts_client, resolve_voice, voice_name_for_locale
from speech_models import SynthesisRequest, SynthesisResult, normalize_text


def synthesize_text(text: str, locale: str = "en-US", voice: Optional[str] = None, audio_format: str = "mp3") -> SynthesisResult:
    client = get_tts_client()
    selected_voice = voice or voice_name_for_locale(locale)
    normalized_text = normalize_text(text)
    request = SynthesisRequest(text=normalized_text, voice=resolve_voice(selected_voice, locale), audio_format=audio_format)
    response = client.synthesize(request)
    audio_bytes = response.audio_bytes
    return SynthesisResult(audio_bytes=audio_bytes, content_type=response.content_type, voice=response.voice, text=normalized_text)


def synthesize_text_base64(text: str, locale: str = "en-US", voice: Optional[str] = None, audio_format: str = "mp3") -> str:
    result = synthesize_text(text=text, locale=locale, voice=voice, audio_format=audio_format)
    return base64.b64encode(result.audio_bytes).decode("ascii")
