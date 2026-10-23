from google.cloud import texttospeech

from speech_client import get_client, get_default_language_code


def select_voice(locale: str | None = None):
    client = get_client()
    response = client.list_voices(language_code=locale or get_default_language_code())
    return [voice.name for voice in response.voices]
