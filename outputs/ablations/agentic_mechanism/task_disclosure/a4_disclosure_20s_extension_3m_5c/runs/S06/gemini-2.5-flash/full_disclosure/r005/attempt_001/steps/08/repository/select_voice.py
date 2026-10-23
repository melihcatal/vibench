import os
from google.cloud import texttospeech

def list_voices(language_code: str = None):
    """Lists the available voices.

    Args:
        language_code: Optional, a BCP-47 language tag (e.g., "en-US", "es-ES").
                       If specified, only voices for that language will be returned.
    """
    client = texttospeech.TextToSpeechClient()

    # The language code to filter for, e.g., "en-US"
    request = texttospeech.ListVoicesRequest(language_code=language_code)

    voices = client.list_voices(request=request).voices

    print(f"Voices available (filtered by language_code='{language_code}' if provided):")
    for voice in voices:
        # Display the voice's name. Example: "en-US-Wavenet-A"
        print(f"  Name: {voice.name}")
        # Display the supported language codes for this voice. Example: "en-US"
        print(f"  Supported languages: {', '.join(voice.language_codes)}")
        # Display the SSML voice gender. Example: "FEMALE"
        print(f"  SSML Voice Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        # Display the natural sample rate hertz. Example: "24000"
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}
")

def select_voice(voice_name: str, language_code: str):
    """Selects a specific voice for synthesis.

    Args:
        voice_name: The name of the voice to select (e.g., "en-US-Wavenet-A").
        language_code: The BCP-47 language tag for the voice (e.g., "en-US").

    Returns:
        A TextToSpeech `VoiceSelectionParams` object.
    """
    return texttospeech.VoiceSelectionParams(
        language_code=language_code,
        name=voice_name
    )

if __name__ == "__main__":
    # Example usage:
    # Set the GOOGLE_APPLICATION_CREDENTIALS environment variable
    # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/path/to/your/key.json"

    print("Listing all available voices:")
    list_voices()

    print("\nListing US English voices:")
    list_voices(language_code="en-US")

    # Example of selecting a voice
    selected = select_voice(voice_name="en-US-Wavenet-C", language_code="en-US")
    print(f"\nSelected voice: {selected.name} with language code {selected.language_code}")
