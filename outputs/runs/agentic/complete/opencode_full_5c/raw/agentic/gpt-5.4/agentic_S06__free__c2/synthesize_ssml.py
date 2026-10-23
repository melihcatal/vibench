from __future__ import annotations

from speech_client import synthesize_ssml_payload
from speech_models import SynthesisResponse


def synthesize_ssml(
    ssml: str,
    audio_format: str = "audio-24khz-160kbitrate-mono-mp3",
    voice: str | None = None,
    locale: str | None = None,
) -> SynthesisResponse:
    if not ssml or not ssml.strip():
        raise ValueError("ssml is required")
    return synthesize_ssml_payload(
        ssml=ssml.strip(), output_format=audio_format, voice=voice, locale=locale
    )
