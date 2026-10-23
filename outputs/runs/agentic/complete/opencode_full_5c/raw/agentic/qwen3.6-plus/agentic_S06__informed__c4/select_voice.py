from speech_client import (
    get_elevenlabs_client,
    get_voice_id,
    list_all_voices,
    normalize_voice_info,
)
from speech_models import VoiceInfo, VoiceSelectionResult


def select_voice(locale: str, voice_name: str = None) -> VoiceSelectionResult:
    client = get_elevenlabs_client()
    all_voices = list_all_voices(client)
    candidates = []
    for v in all_voices:
        candidates.append(
            VoiceInfo(
                voice_id=v["voice_id"],
                name=v["name"],
                category=v["category"],
                labels=v["labels"],
                preview_url=v.get("preview_url"),
            )
        )
    selected_voice_id = get_voice_id(client, voice_name=voice_name, locale=locale)
    selected_info = None
    for v in candidates:
        if v.voice_id == selected_voice_id:
            selected_info = v
            break
    if selected_info is None and candidates:
        selected_info = candidates[0]
    return VoiceSelectionResult(
        selected_voice=selected_info,
        locale=locale,
        all_candidates=candidates,
    )


def list_voices_for_locale(locale: str):
    client = get_elevenlabs_client()
    all_voices = list_all_voices(client)
    locale_lower = locale.lower()
    matching = []
    for v in all_voices:
        labels = v.get("labels", {})
        accent = labels.get("accent", "").lower()
        language = labels.get("language", "").lower()
        description = labels.get("description", "").lower()
        if (
            locale_lower in accent
            or locale_lower in language
            or locale_lower in description
        ):
            matching.append(
                VoiceInfo(
                    voice_id=v["voice_id"],
                    name=v["name"],
                    category=v["category"],
                    labels=labels,
                    preview_url=v.get("preview_url"),
                )
            )
    return matching
