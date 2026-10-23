from google.cloud import texttospeech
from speech_client import get_text_to_speech_client
from typing import List, Dict, Any

def select_voice(language_code: str = None) -> List[Dict[str, Any]]:
    client = get_text_to_speech_client()
    voices = client.list_voices(language_code=language_code).voices
    
    voice_list = []
    for voice in voices:
        voice_list.append({
            "name": voice.name,
            "language_codes": list(voice.language_codes),
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        })
    return voice_list

if __name__ == '__main__':
    # Example usage
    print("Available English (US) voices:")
    en_us_voices = select_voice(language_code="en-US")
    for voice in en_us_voices[:5]: # Print first 5 for brevity
        print(f"  Name: {voice['name']}, Gender: {voice['ssml_gender']}")

    print("\nAvailable Japanese voices:")
    ja_voices = select_voice(language_code="ja-JP")
    for voice in ja_voices[:5]: # Print first 5 for brevity
        print(f"  Name: {voice['name']}, Gender: {voice['ssml_gender']}")
