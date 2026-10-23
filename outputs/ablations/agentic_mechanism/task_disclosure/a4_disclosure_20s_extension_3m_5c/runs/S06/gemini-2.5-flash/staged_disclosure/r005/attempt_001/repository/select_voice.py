import os
from google.cloud import texttospeech

def list_voices():
    """Lists the available voices."""
    client = texttospeech.TextToSpeechClient()

    voices = client.list_voices().voices

    for voice in voices:
        print(f"Name: {voice.name}")
        print(f"  SSML Voice Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}")
        print(f"  Supported languages: {voice.language_codes}")

def select_voice(language_code: str):
    """Selects a voice for a target locale."""
    client = texttospeech.TextToSpeechClient()

    # Perform the list voices request
    voices = client.list_voices(language_code=language_code).voices

    if not voices:
        print(f"No voices found for language code: {language_code}")
        return

    print(f"Available voices for {language_code}:")
    for voice in voices:
        print(f"  Name: {voice.name}, Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")

    # You can choose a specific voice from the listed voices
    # For example, to select the first voice:
    if voices:
        chosen_voice_name = voices[0].name
        chosen_voice_gender = texttospeech.SsmlVoiceGender(voices[0].ssml_gender).name
        print(f"
Selected voice: Name={chosen_voice_name}, Gender={chosen_voice_gender}")
    else:
        print("No voices to select.")

if __name__ == "__main__":
    # To use this, you need to set up Google Cloud authentication.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    print("Listing all available voices:")
    list_voices()

    print("\nSelecting voices for 'en-US':")
    select_voice("en-US")

    print("\nSelecting voices for 'fr-FR':")
    select_voice("fr-FR")
