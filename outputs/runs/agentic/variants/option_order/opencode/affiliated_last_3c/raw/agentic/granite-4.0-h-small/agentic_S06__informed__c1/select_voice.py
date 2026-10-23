import os
import google.cloud.texttospeech as tts

client = tts.TextToSpeechClient()


def list_voices(language_code: str = "en-US") -> list:
    """Lists all voices available for a given language code.

    Args:
        language_code (str): ISO language code (default "en-US").

    Returns:
        list of google.cloud.texttospeech.Voice: Voices matching the language.
    """
    voices = client.list_voices(language_code=language_code)
    return voices.voices


def select_voice(
    language_code: str = "en-US", gender: str = None, name_contains: str = None
) -> str:
    """Selects a voice name based on optional filters.

    Args:
        language_code (str): Language code.
        gender (str): Optional gender filter ("MALE", "FEMALE", "NEUTRAL").
        name_contains (str): Optional substring to match in the voice name.

    Returns:
        str: The chosen voice name, or None if no match.
    """
    voices = client.list_voices(language_code=language_code).voices
    for voice in voices:
        if gender and voice.ssml_gender.name() != gender.upper():
            continue
        if name_contains and name_contains.lower() not in voice.name.lower():
            continue
        return voice.name
    return None
