from google.cloud import texttospeech
from speech_client import get_tts_client


def select_voice(language_code: str) -> texttospeech.Voice | None:
    """
    Lists available voices for a given language and selects one.

    Args:
        language_code: The language code to filter voices by (e.g., 'en-US').

    Returns:
        A Voice object or None if no voices are found.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)

    if not response.voices:
        return None

    # Simple selection criteria: return the first available voice
    return response.voices[0]


def get_voice_names_by_language(language_code: str) -> list[str]:
    """
    Gets a list of voice names for a specific language.
    """
    client = get_tts_client()
    response = client.list_voices(language_code=language_code)
    return [voice.name for voice in response.voices]
