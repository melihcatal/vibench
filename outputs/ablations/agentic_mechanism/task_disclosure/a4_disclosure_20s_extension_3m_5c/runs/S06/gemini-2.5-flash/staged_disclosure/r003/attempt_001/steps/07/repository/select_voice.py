import os
from google.cloud import texttospeech

def list_voices(language_code="en-US"):
    """Lists the available voices for a given language code."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices

    print(f"Voices for language code {language_code}:")
    for voice in voices:
        print(f"Name: {voice.name}")
        print(f"SsmlGender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"NaturalSampleRateHertz: {voice.natural_sample_rate_hertz}")
        print(f"SupportedLanguageCodes: {voice.language_codes}\n")

def select_voice(language_code="en-US", ssml_gender="FEMALE"):
    """Selects a voice based on language code and SSML gender."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices

    selected_voice = None
    for voice in voices:
        if texttospeech.SsmlVoiceGender(voice.ssml_gender).name == ssml_gender.upper():
            selected_voice = voice
            break

    if selected_voice:
        print(f"Selected Voice for {language_code} with {ssml_gender} gender:")
        print(f"Name: {selected_voice.name}")
        print(f"SsmlGender: {texttospeech.SsmlVoiceGender(selected_voice.ssml_gender).name}")
        print(f"NaturalSampleRateHertz: {selected_voice.natural_sample_rate_hertz}")
        print(f"SupportedLanguageCodes: {selected_voice.language_codes}")
        return selected_voice
    else:
        print(f"No voice found for {language_code} with {ssml_gender} gender.")
        return None

if __name__ == "__main__":
    # To run this example, you need to set up Google Cloud authentication.
    # For example, by setting the GOOGLE_APPLICATION_CREDENTIALS environment variable:
    # export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/keyfile.json"

    # List all available voices (default en-US)
    list_voices()

    print("\n--- Selecting a specific voice ---")
    # Select a female voice for en-US
    select_voice(language_code="en-US", ssml_gender="FEMALE")

    print("\n--- Selecting another specific voice ---")
    # Select a male voice for en-GB
    select_voice(language_code="en-GB", ssml_gender="MALE")
