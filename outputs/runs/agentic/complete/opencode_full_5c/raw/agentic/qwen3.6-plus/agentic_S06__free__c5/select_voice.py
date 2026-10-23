from typing import Optional, List
from speech_client import get_tts_client, list_voices, get_default_voice_for_locale
from speech_models import VoiceInfo, VoiceListResponse, normalize_voice_response


def select_voice(
    locale: str = "en-US",
    gender: Optional[str] = None,
    name_pattern: Optional[str] = None,
    prefer_neural: bool = True,
) -> VoiceInfo:
    client = get_tts_client()
    raw_voices = list_voices(client, language_code=locale)
    voice_list = normalize_voice_response(raw_voices)

    if prefer_neural:
        voice_list = voice_list.filter_by_name_pattern("Neural")

    if gender:
        voice_list = voice_list.filter_by_gender(gender)

    if name_pattern:
        voice_list = voice_list.filter_by_name_pattern(name_pattern)

    selected = voice_list.get_first()
    if selected is None:
        fallback_name = get_default_voice_for_locale(locale)
        selected = VoiceInfo(
            name=fallback_name,
            language_code=locale,
            ssml_gender="NEUTRAL",
        )
    return selected


def list_available_voices(locale: Optional[str] = None) -> VoiceListResponse:
    client = get_tts_client()
    raw_voices = list_voices(client, language_code=locale)
    return normalize_voice_response(raw_voices)


def get_recommended_voice(locale: str, gender: Optional[str] = None) -> VoiceInfo:
    default_name = get_default_voice_for_locale(locale)
    client = get_tts_client()
    raw_voices = list_voices(client, language_code=locale)
    voice_list = normalize_voice_response(raw_voices)

    if gender:
        voice_list = voice_list.filter_by_gender(gender)

    for voice in voice_list.voices:
        if voice.name == default_name:
            return voice

    selected = voice_list.get_first()
    if selected:
        return selected

    return VoiceInfo(
        name=default_name,
        language_code=locale,
        ssml_gender=gender or "NEUTRAL",
    )
