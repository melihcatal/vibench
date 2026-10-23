from google.cloud import texttospeech

from speech_client import get_client


def list_voices(locale: str = None):
    client = get_client()
    response = client.list_voices(language_code=locale)
    return [voice.name for voice in response.voices]


def select_voice(locale: str, preferred: str = None):
    voices = list_voices(locale)
    if preferred and preferred in voices:
        return preferred
    return voices[0] if voices else None
