from google.cloud import texttospeech
import os
from typing import List, Dict, Any

def list_voices(language_code: str = "en-US") -> List[Dict[str, Any]]:
    """Lists available voices for a given language code using Google Cloud Text-to-Speech.

    Args:
        language_code: The BCP-47 language code (e.g., "en-US").

    Returns:
        A list of dictionaries, where each dictionary represents a voice.
    """
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_info = {
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }
        voice_list.append(voice_info)
    return voice_list

def select_voice_by_criteria(language_code: str, gender: str = None, name_substring: str = None) -> Dict[str, Any]:
    """Selects a voice based on criteria.

    Args:
        language_code: The BCP-47 language code (e.g., "en-US").
        gender: Optional. "MALE", "FEMALE", or "NEUTRAL".
        name_substring: Optional. A substring to look for in the voice name.

    Returns:
        A dictionary representing the selected voice, or None if no voice matches.
    """
    available_voices = list_voices(language_code)
    for voice in available_voices:
        if gender and voice["ssml_gender"] != gender.upper():
            continue
        if name_substring and name_substring not in voice["name"]:
            continue
        return voice
    return None


if __name__ == '__main__':
    # Example usage
    print("\nAvailable English (US) voices:")
    us_voices = list_voices("en-US")
    for voice in us_voices[:5]: # Print first 5 for brevity
        print(f"  Name: {voice['name']}, Gender: {voice['ssml_gender']}, Sample Rate: {voice['natural_sample_rate_hertz']}")

    print("\nSelecting a female Wavenet voice for en-US:")
    selected_female_voice = select_voice_by_criteria("en-US", gender="FEMALE", name_substring="Wavenet")
    if selected_female_voice:
        print(f"  Selected voice: {selected_female_voice['name']}")
    else:
        print("  No matching voice found.")
