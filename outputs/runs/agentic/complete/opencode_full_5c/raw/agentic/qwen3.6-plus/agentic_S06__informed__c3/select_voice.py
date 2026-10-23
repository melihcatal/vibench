from typing import List, Optional
from speech_client import get_client
from speech_models import VoiceInfo, normalize_voice_info


def list_vvoices(locale: Optional[str] = None) -> List[VoiceInfo]:
    client = get_client()
    voices_response = client.voices.get_all()
    voices = []
    for v in voices_response.voices:
        voice_data = {
            "voice_id": v.voice_id,
            "name": v.name,
            "labels": v.labels or {},
            "preview_url": v.preview_url or "",
            "category": v.category or "",
        }
        voice_info = normalize_voice_info(voice_data)
        if locale:
            locale_lower = locale.lower()
            labels = voice_data.get("labels", {})
            matches = any(locale_lower in str(val).lower() for val in labels.values())
            if not matches:
                continue
        voices.append(voice_info)
    return voices


def select_voice(
    locale: str, preferred_gender: Optional[str] = None
) -> Optional[VoiceInfo]:
    voices = list_vvoices(locale=locale)
    if not voices:
        return None
    if preferred_gender:
        gender_lower = preferred_gender.lower()
        for v in voices:
            if v.gender.lower() == gender_lower:
                return v
    return voices[0]
