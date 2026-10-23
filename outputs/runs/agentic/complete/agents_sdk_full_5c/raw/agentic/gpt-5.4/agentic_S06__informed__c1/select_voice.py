from __future__ import annotations

from typing import List, Optional

from google.cloud import texttospeech

from speech_client import get_tts_client
from speech_models import VoiceOption, normalize_voice


GOOGLE_TTS_MODEL_FAMILY = "Chirp3-HD"


def list_voices_for_locale(locale: str) -> List[VoiceOption]:
    client = get_tts_client()
    response = client.list_voices(language_code=locale)
    return [normalize_voice(voice) for voice in response.voices]


def select_voice(locale: str, preferred_gender: Optional[str] = None, name_contains: Optional[str] = None) -> VoiceOption:
    voices = list_voices_for_locale(locale)
    filtered = voices
    if preferred_gender:
        filtered = [v for v in filtered if (v.ssml_gender or "").upper() == preferred_gender.upper()]
    if name_contains:
        filtered = [v for v in filtered if name_contains.lower() in v.name.lower()]
    if not filtered:
        raise LookupError(f"No Google Cloud Text-to-Speech voices found for locale={locale}")
    return sorted(
        filtered,
        key=lambda v: (
            0 if "Neural2" in v.name else 1,
            0 if "Wavenet" in v.name else 1,
            v.name,
        ),
    )[0]
