import os
from google.cloud import texttospeech

def list_voices(language_code: str = "en-US"):
    """Lists available voices for a given language code using Google Cloud Text-to-Speech."""
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code=language_code).voices

    print(f"Voices for {language_code}:")
    for voice in voices:
        print(f"  Name: {voice.name}")
        print(f"  SSML Voice Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}")
        print(f"  Supported language codes: {voice.language_codes}")
        print("\n")

    return voices

if __name__ == '__main__':
    # Ensure GOOGLE_APPLICATION_CREDENTIALS is set for authentication
    # Example usage:
    # list_voices("en-US")
    # list_voices("es-ES")
    pass
