from __future__ import annotations

from typing import List, Optional

from speech_client import build_speech_client
from speech_models import VoiceSelection, VoiceSummary

try:
    from google.cloud import texttospeech
except Exception:  # pragma: no cover
    texttospeech = None


def list_voices(locale: Optional[str] = None) -> List[VoiceSummary]:
    """List available Google Cloud Text-to-Speech voices, optionally filtered by locale."""
    client = build_speech_client()
    if texttospeech is None:
        raise RuntimeError("google-cloud-texttospeech is required for list_voices")

    response = client.list_voices(language_code=locale) if locale else client.list_voices()
    summaries: List[VoiceSummary] = []
    for voice in response.voices:
        summaries.append(
            VoiceSummary(
                name=voice.name,
                locales=list(getattr(voice, "language_codes", [])),
                gender=str(getattr(voice, "ssml_gender", "")),
            )
        )
    return summaries


def select_voice(locale: str, preferred_name: Optional[str] = None) -> VoiceSelection:
    voices = list_voices(locale)
    if preferred_name:
        for voice in voices:
            if voice.name == preferred_name:
                return VoiceSelection(name=voice.name, locale=locale)
    if not voices:
        raise ValueError(f"No voices available for locale {locale}")
    return VoiceSelection(name=voices[0].name, locale=locale)
