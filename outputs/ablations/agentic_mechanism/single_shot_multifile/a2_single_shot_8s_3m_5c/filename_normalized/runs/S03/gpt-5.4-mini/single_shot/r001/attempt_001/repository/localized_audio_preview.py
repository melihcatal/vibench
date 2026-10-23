from translation_client import get_translation_client

_PROVIDER = "google"


def localized_audio_preview(text: str, language_code: str) -> bytes:
    client = get_translation_client()
    return client.generate_audio_preview(text, language_code)
