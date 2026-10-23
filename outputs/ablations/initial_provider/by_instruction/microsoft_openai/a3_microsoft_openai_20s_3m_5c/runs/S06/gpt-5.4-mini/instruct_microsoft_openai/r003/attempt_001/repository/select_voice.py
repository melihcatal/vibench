from speech_client import client
from speech_models import normalize_locale, normalize_voice


def list_voices(locale: str = None):
    _ = normalize_locale(locale)
    return ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]


def select_voice(locale: str, preferred: str = None) -> str:
    voices = list_voices(locale)
    if preferred:
        preferred = normalize_voice(preferred)
        if preferred in voices:
            return preferred
    return voices[0]


def voice_client():
    return client()
