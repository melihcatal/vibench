from google.cloud import speech


def get_speech_client(config=None):
    config = config or {}
    return speech.SpeechClient()


def get_language_code(payload, config=None):
    config = config or {}
    return payload.get("language_code") or config.get("language_code") or "en-US"
