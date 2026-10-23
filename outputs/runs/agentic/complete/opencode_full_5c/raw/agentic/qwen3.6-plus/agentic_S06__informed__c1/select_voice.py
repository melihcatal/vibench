import httpx
from typing import List, Optional
from speech_client import build_json_headers, ELEVENLABS_API_BASE
from speech_models import VoiceInfo, normalize_voice_info


def list_voices(api_key: str = None) -> List[VoiceInfo]:
    headers = build_json_headers(api_key)
    url = f"{ELEVENLABS_API_BASE}/voices"
    with httpx.Client(timeout=30.0) as client:
        response = client.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
    voices = data.get("voices", [])
    return [normalize_voice_info(v) for v in voices]


def select_voice(
    locale: str = "en-US",
    gender: Optional[str] = None,
    category: Optional[str] = None,
    api_key: str = None,
) -> VoiceInfo:
    voices = list_voices(api_key)
    locale_lower = locale.lower()
    candidates = []
    for voice in voices:
        labels = voice.labels or {}
        accent = labels.get("accent", "").lower()
        language = labels.get("language", "").lower()
        if locale_lower in accent or locale_lower in language:
            candidates.append(voice)
    if not candidates:
        candidates = [v for v in voices if v.category == "premade"]
    if gender:
        gender_filtered = [
            v
            for v in candidates
            if v.labels.get("gender", "").lower() == gender.lower()
        ]
        if gender_filtered:
            candidates = gender_filtered
    if category:
        cat_filtered = [v for v in candidates if v.category.lower() == category.lower()]
        if cat_filtered:
            candidates = cat_filtered
    if not candidates:
        candidates = voices
    return (
        candidates[0]
        if candidates
        else VoiceInfo(
            voice_id="",
            name="",
            category="",
            description="",
        )
    )
