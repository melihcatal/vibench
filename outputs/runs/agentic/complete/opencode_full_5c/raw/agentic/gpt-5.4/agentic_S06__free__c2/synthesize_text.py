from __future__ import annotations

from speech_client import build_ssml, choose_voice, synthesize_ssml_payload
from speech_models import (
    SynthesisRequest,
    SynthesisResponse,
    ensure_text,
    normalize_locale,
)


def synthesize_text(
    text: str,
    locale: str = "en-US",
    voice: str | None = None,
    audio_format: str = "audio-16khz-128kbitrate-mono-mp3",
) -> SynthesisResponse:
    normalized_locale = normalize_locale(locale)
    resolved_text = ensure_text(text)
    selected_voice = voice or choose_voice(normalized_locale).name
    request = SynthesisRequest(
        text=resolved_text,
        locale=normalized_locale,
        voice=selected_voice,
        audio_format=audio_format,
    )
    ssml = build_ssml(request)
    return synthesize_ssml_payload(
        ssml=ssml,
        output_format=request.audio_format,
        voice=selected_voice,
        locale=normalized_locale,
    )
