import os
from google.cloud import texttospeech


def list_voices(language_code: str = "en") -> list:
    """List available voices filtered by language.

    Args:
        language_code (str): Language identifier ('en', 'es', etc.).

    Returns:
        list: Available voices for the language.
    """
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv(
        "GOOGLE_APPLICATION_CREDENTIALS", "path/to/credentials.json"
    )
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices
    return [voice.name for voice in voices]


def select_voice(language_code: str = "en") -> str:
    """Prompt user to select a voice for the given language.

    Args:
        language_code (str): Language identifier.

    Returns:
        str: Selected voice name.
    """
    voices = list_voices(language_code)
    for i, v in enumerate(voices, 1):
        print(f"{i}. {v}")
    choice = int(input("Select a voice (number): "))
    return voices[choice - 1]
