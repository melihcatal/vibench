from speech_client import list_voices


def select_voice(locale: str | None = None):
    voices = list_voices(locale)
    return voices[0] if voices else None
