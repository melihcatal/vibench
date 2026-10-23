import os
from google.cloud import texttospeech

def list_voices(language_code: str = None):
    """Lists the available voices for a given language code.
    If no language_code is specified, it lists all available voices.
    """
    client = texttospeech.TextToSpeechClient()

    # Performs the list voices request
    voices = client.list_voices(language_code=language_code).voices

    print(f"Voices for language code: {language_code if language_code else 'All'}:")
    for voice in voices:
        print(f"  Name: {voice.name}")
        print(f"  SSML Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}")
        print(f"  Supported language codes: {voice.language_codes}")
        print("-" * 20)

def select_voice(language_code: str, ssml_gender: str = None, name: str = None):
    """Selects a voice based on language code, gender, and/or name."""
    client = texttospeech.TextToSpeechClient()

    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=getattr(texttospeech.SsmlVoiceGender, ssml_gender.upper()) if ssml_gender else None,
        name=name
    )

    # This is a simplified selection, as list_voices is usually used to discover.
    # To actually "select" for a synthesis, you'd use this in a synthesize request.
    print(f"Attempting to select voice with Language Code: {language_code}")
    if ssml_gender:
        print(f"  SSML Gender: {ssml_gender}")
    if name:
        print(f"  Name: {name}")

    # For demonstration, we'll just show what the selection parameters would be.
    # In a real application, this would be part of a synthesize_speech call.
    print(f"Voice selection parameters created: {voice_selection_params}")

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    # List all available voices
    list_voices()

    # List voices for a specific language code (e.g., "en-US")
    list_voices(language_code="en-US")

    # Select a specific voice (this part demonstrates parameter creation, not actual voice synthesis)
    select_voice(language_code="en-US", ssml_gender="FEMALE", name="en-US-Wavenet-F")
