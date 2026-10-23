from google.cloud import texttospeech

from speech_client import client


def select_voice(language_code: str, name: str | None = None):
    c = client()
    voices = c.list_voices(language_code=language_code).voices
    if name:
        for voice in voices:
            if voice.name == name:
                return voice
    return voices[0] if voices else None
