# [SAME-SCENARIO] select_voice.py
# Lists or selects a voice for a target locale using Azure Speech TTS

import os
from azure.cognitiveservices.speech import SpeechConfig

AZURE_SPEECH_KEY = os.getenv("AZURE_SPEECH_KEY")
AZURE_SPEECH_REGION = os.getenv("AZURE_SPEECH_REGION")


def list_voices(locale: str = "en-US") -> list:
    """List available voices for a given locale.

    Args:
        locale (str): Locale code (e.g., "en-US").

    Returns:
        list: A list of voice names available for the locale.
    """
    speech_config = SpeechConfig(
        subscription=AZURE_SPEECH_KEY, region=AZURE_SPEECH_REGION
    )
    voices = speech_config.get_voices_list()
    # Filter voices by locale
    return [voice.name for voice in voices if voice.locale_language_tag == locale]


def select_voice_by_name(name: str) -> str:
    """Return the selected voice name if it exists.

    Args:
        name (str): Desired voice name.

    Returns:
        str: The selected voice name or raises if not found.
    """
    available = list_voices()
    if name in available:
        return name
    raise ValueError(f"Voice '{name}' not available. Choose from {available}")


# Example usage
if __name__ == "__main__":
    print("Available voices for en-US:", list_voices("en-US"))
    selected = select_voice_by_name("en-US-JennyNeural")
    print("Selected voice:", selected)
