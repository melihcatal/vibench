import os
from typing import List, Dict
from google.cloud import texttospeech

def list_available_voices(language_code: str = None) -> List[Dict]:
    """Lists available voices for a given language code using Google Cloud Text-to-Speech.

    Args:
        language_code: The BCP-47 language code to filter voices by (e.g., "en-US").
                       If None, lists all available voices.

    Returns:
        A list of dictionaries, each representing an available voice.
    """
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_list.append({
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        })
    return voice_list

def select_voice_for_locale(language_code: str, preferred_gender: str = None) -> Dict:
    """Selects a voice for a target locale based on preferences.

    Args:
        language_code: The BCP-47 language code (e.g., "en-US").
        preferred_gender: Optional. "MALE", "FEMALE", "NEUTRAL" to prefer a gender.

    Returns:
        A dictionary representing the selected voice, or an empty dict if none found.
    """
    available_voices = list_available_voices(language_code=language_code)

    if not available_voices:
        return {}

    # Prioritize Wavenet voices if available
    wavenet_voices = [v for v in available_voices if "Wavenet" in v["name"]]
    if wavenet_voices:
        available_voices = wavenet_voices

    # Filter by preferred gender
    if preferred_gender:
        gender_filtered_voices = [v for v in available_voices if v["gender"] == preferred_gender.upper()]
        if gender_filtered_voices:
            return gender_filtered_voices[0]

    # Return the first available voice if no specific gender preference or match
    return available_voices[0]
