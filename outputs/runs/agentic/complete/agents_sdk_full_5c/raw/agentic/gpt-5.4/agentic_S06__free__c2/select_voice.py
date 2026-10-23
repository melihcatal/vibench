from __future__ import annotations

from typing import List, Optional

from speech_client import GoogleSpeechClient
from speech_models import VoiceOption


def list_voices_for_locale(locale: str) -> List[VoiceOption]:
    client = GoogleSpeechClient()
    response = client.list_voices(language_code=locale)
    voices = response.get("voices", [])
    return [
        VoiceOption(
            name=item["name"],
            language_codes=item.get("languageCodes", []),
            ssml_gender=item.get("ssmlGender"),
            natural_sample_rate_hertz=item.get("naturalSampleRateHertz"),
        )
        for item in voices
    ]


def select_voice(locale: str, preferred_gender: Optional[str] = None) -> Optional[VoiceOption]:
    candidates = list_voices_for_locale(locale)
    if preferred_gender:
        gender_matches = [v for v in candidates if (v.ssml_gender or "").upper() == preferred_gender.upper()]
        if gender_matches:
            return sorted(gender_matches, key=lambda v: ("Neural2" not in v.name, "Studio" not in v.name, v.name))[0]
    if not candidates:
        return None
    return sorted(candidates, key=lambda v: ("Neural2" not in v.name, "Studio" not in v.name, v.name))[0]
