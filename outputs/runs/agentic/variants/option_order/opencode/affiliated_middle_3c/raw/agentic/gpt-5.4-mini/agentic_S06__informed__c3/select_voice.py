from speech_client import list_voices


def select_voice(locale: str):
    voices = list_voices()
    locale_key = locale.replace("_", "-").lower()
    for voice in voices:
        labels = getattr(voice, "labels", {}) or {}
        if any(
            str(v).replace("_", "-").lower().startswith(locale_key.split("-")[0])
            for v in labels.values()
        ):
            return voice
    return voices[0] if voices else None


def list_voice_names(locale: str | None = None):
    voices = list_voices()
    if not locale:
        return [getattr(v, "name", "") for v in voices]
    selected = select_voice(locale)
    return [getattr(selected, "name", "")] if selected else []
