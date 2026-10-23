from __future__ import annotations

from typing import List, Optional

from speech_client import GoogleSpeechClient
from speech_models import VoiceSummary, normalize_voice_record


def list_voices(locale: Optional[str] = None) -> List[VoiceSummary]:
    client = GoogleSpeechClient()
    params = {"languageCode": locale} if locale else None
    data = client.get("/voices", params=params)
    return [normalize_voice_record(v) for v in data.get("voices", [])]


def select_voice_for_locale(locale: str, preferred_gender: Optional[str] = None) -> Optional[VoiceSummary]:
    voices = list_voices(locale)
    if preferred_gender:
        for voice in voices:
            if voice.gender == preferred_gender:
                return voice
    for voice in voices:
        if locale in voice.language_codes:
            return voice
    return voices[0] if voices else None
