import os
from google.cloud import texttospeech

def list_voices(language_code: str = "en-US"):
    """Lists available voices for a target locale using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code=language_code).voices

    voice_list = []
    for voice in voices:
        voice_info = {
            "name": voice.name,
            "language_codes": voice.language_codes,
            "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
            "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
        }
        voice_list.append(voice_info)
    return voice_list

if __name__ == "__main__":
    # Example usage (ensure GOOGLE_APPLICATION_CREDENTIALS is set)
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"
    en_us_voices = list_voices("en-US")
    print(f"Available en-US voices ({len(en_us_voices)}):\n")
    for voice in en_us_voices[:5]: # Print first 5 voices as an example
        print(voice)
    print("...")
