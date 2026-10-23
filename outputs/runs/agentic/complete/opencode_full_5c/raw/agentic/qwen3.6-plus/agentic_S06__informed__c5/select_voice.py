from speech_client import get_elevenlabs_client
from speech_models import VoiceInfo, normalize_voice_data, VoiceSelectionResult


def list_voices() -> list[VoiceInfo]:
    client = get_elevenlabs_client()
    voices_response = client.voices.get_all()
    return [normalize_voice_data(v) for v in voices_response.voices]


def select_voice_by_locale(locale: str) -> VoiceSelectionResult:
    client = get_elevenlabs_client()
    voices_response = client.voices.get_all()

    locale_lower = locale.lower()
    for voice in voices_response.voices:
        labels = voice.labels or {}
        for key, value in labels.items():
            if locale_lower in key.lower() or locale_lower in str(value).lower():
                return VoiceSelectionResult(
                    voice_id=voice.voice_id,
                    name=voice.name,
                    locale=locale,
                    gender=labels.get("gender", "neutral"),
                )

    if voices_response.voices:
        first = voices_response.voices[0]
        labels = first.labels or {}
        return VoiceSelectionResult(
            voice_id=first.voice_id,
            name=first.name,
            locale=locale,
            gender=labels.get("gender", "neutral"),
        )

    raise ValueError(f"No voices available for locale {locale}")


def get_voice_details(voice_id: str) -> VoiceInfo:
    client = get_elevenlabs_client()
    voice = client.voices.get(voice_id=voice_id)
    return normalize_voice_data(voice)
