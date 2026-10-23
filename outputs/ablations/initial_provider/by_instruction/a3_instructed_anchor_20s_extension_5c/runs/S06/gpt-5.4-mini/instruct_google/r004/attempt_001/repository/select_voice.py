from google.cloud import texttospeech

from speech_client import build_client, load_config


def select_voice(locale: str | None = None, name: str | None = None):
    client = build_client()
    cfg = load_config()
    target_locale = locale or cfg.default_language_code
    voices = client.list_voices(language_code=target_locale).voices
    if name:
        for voice in voices:
            if voice.name == name:
                return voice
    return voices[0] if voices else None
