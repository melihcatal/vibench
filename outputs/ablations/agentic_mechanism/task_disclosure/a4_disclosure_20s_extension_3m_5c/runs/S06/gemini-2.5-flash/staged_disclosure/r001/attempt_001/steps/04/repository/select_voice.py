
import os
from google.cloud import texttospeech

def list_voices():
    """Lists the available voices."""
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices().voices

    for voice in voices:
        # Display the SSML Voice Gender
        ssml_gender = texttospeech.SsmlVoiceGender(voice.ssml_gender).name

        # Display the supported language codes for this voice.
        for language_code in voice.language_codes:
            print(f"Name: {{voice.name}}, Supported language: {{language_code}}, SSML Gender: {{ssml_gender}}")


def select_voice(target_locale: str):
    """Selects a voice for a target locale."""
    client = texttospeech.TextToSpeechClient()

    voices = client.list_voices().voices
    
    found_voice = None
    for voice in voices:
        if target_locale in voice.language_codes:
            found_voice = voice
            break

    if found_voice:
        ssml_gender = texttospeech.SsmlVoiceGender(found_voice.ssml_gender).name
        print(f"Selected Voice: {{found_voice.name}}, Supported language: {{target_locale}}, SSML Gender: {{ssml_gender}}")
        return found_voice.name
    else:
        print(f"No voice found for locale: {{target_locale}}")
        return None

if __name__ == "__main__":
    # To run this script, you need to set up Google Cloud authentication.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    print("Listing all available voices:")
    list_voices()

    print("\nSelecting a voice for 'en-US':")
    select_voice("en-US")

    print("\nSelecting a voice for 'es-ES':")
    select_voice("es-ES")

    print("\nSelecting a voice for 'fr-FR':")
    select_voice("fr-FR")
