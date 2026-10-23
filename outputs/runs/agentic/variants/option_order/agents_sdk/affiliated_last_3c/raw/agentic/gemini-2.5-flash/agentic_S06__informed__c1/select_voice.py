from google.cloud import texttospeech
import os
from typing import List, Dict

def list_available_voices(language_code: str = "en-US") -> List[Dict]:
    """Lists available voices for a given language code using Google Cloud Text-to-Speech.
    
    Args:
        language_code: The desired language code (e.g., "en-US", "es-ES").
        
    Returns:
        A list of dictionaries, each representing an available voice.
    """
    client = texttospeech.TextToSpeechClient()
    
    # Perform the list voices request
    response = client.list_voices(language_code=language_code)
    
    voices_info = []
    for voice in response.voices:
        voices_info.append({
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz
        })
        
    return voices_info

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/credentials.json"
    
    print("Available English (US) voices:")
    english_voices = list_available_voices("en-US")
    for voice in english_voices[:5]: # Print first 5 for brevity
        print(f"  Name: {voice['name']}, Gender: {voice['ssml_gender']}, Sample Rate: {voice['natural_sample_rate_hertz']}")

    print("\nAvailable Spanish (Spain) voices:")
    spanish_voices = list_available_voices("es-ES")
    for voice in spanish_voices[:5]: # Print first 5 for brevity
        print(f"  Name: {voice['name']}, Gender: {voice['ssml_gender']}, Sample Rate: {voice['natural_sample_rate_hertz']}")
