from google.cloud import texttospeech
import os
from typing import List, Dict, Any

def list_voices(language_code: str = "en-US") -> List[Dict[str, Any]]:
    """Lists available voices for a given language code using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code=language_code).voices

    voice_details = []
    for voice in voices:
        voice_details.append({
            "name": voice.name,
            "language_codes": voice.language_codes,
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        })
    return voice_details

def select_voice_by_name(voice_name: str, language_code: str = "en-US") -> Dict[str, Any] or None:
    """Selects a specific voice by name for a given language code."""
    all_voices = list_voices(language_code)
    for voice in all_voices:
        if voice["name"] == voice_name:
            return voice
    return None

if __name__ == "__main__":
    if "GOOGLE_APPLICATION_CREDENTIALS" not in os.environ:
        print("Please set the GOOGLE_APPLICATION_CREDENTIALS environment variable.")
    else:
        print("Listing voices for en-US:")
        voices = list_voices("en-US")
        for voice in voices[:5]:  # Print first 5 voices for brevity
            print(f"  Name: {voice['name']}, Gender: {voice['ssml_gender']}")

        selected = select_voice_by_name("en-US-Wavenet-C")
        if selected:
            print(f"\nSelected voice: {selected['name']}")
        else:
            print("\nVoice en-US-Wavenet-C not found.")
