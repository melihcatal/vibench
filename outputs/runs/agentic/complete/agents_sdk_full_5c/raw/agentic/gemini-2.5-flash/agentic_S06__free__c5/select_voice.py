
from google.cloud import texttospeech_v1 as texttospeech
import os
from typing import List, Dict, Any

def list_voices(language_code: str = "en-US") -> List[Dict[str, Any]]:
    """Lists available voices for a given language code using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    # Performs list voices request
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

def select_voice_by_criteria(language_code: str, ssml_gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL, preferred_name_substring: str = None) -> Dict[str, Any]:
    """Selects a voice based on criteria from the list of available voices."""
    available_voices = list_voices(language_code)
    for voice in available_voices:
        if voice["ssml_gender"] == ssml_gender.name:
            if preferred_name_substring and preferred_name_substring in voice["name"]:
                return voice
            elif not preferred_name_substring:
                return voice
    return {}

if __name__ == '__main__':
    print("Listing all en-US voices:")
    en_us_voices = list_voices("en-US")
    for voice in en_us_voices:
        print(f"  Voice: {voice['name']}, Gender: {voice['ssml_gender']}, Sample Rate: {voice['natural_sample_rate_hertz']} Hz")

    print("\nSelecting a female voice for en-US with Wavenet in name:")
    selected_voice = select_voice_by_criteria("en-US", texttospeech.SsmlVoiceGender.FEMALE, "Wavenet")
    if selected_voice:
        print(f"  Selected Voice: {selected_voice['name']}")
    else:
        print("  No matching voice found.")
