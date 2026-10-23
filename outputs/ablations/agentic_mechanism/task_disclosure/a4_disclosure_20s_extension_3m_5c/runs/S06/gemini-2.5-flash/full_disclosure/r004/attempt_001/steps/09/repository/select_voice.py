from google.cloud import texttospeech

def list_voices(language_code: str = None):
    """Lists the available voices.
    Args:
        language_code: Optional. The BCP-47 language code to filter voices by.
    """
    client = texttospeech.TextToSpeechClient()
    response = client.list_voices(language_code=language_code)
    voices = sorted(response.voices, key=lambda voice: voice.name)

    print(f"Available Voices ({len(voices)}):")
    for voice in voices:
        print(f"  Name: {voice.name}")
        print(f"  Supported language codes: {voice.language_codes}")
        print(f"  SSML Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}\n")

def select_voice(language_code: str, ssml_gender: texttospeech.SsmlVoiceGender = None) -> texttospeech.VoiceSelectionParams:
    """Selects a voice based on language code and optional SSML gender.
    Args:
        language_code: The BCP-47 language code to select a voice for (e.g., "en-US").
        ssml_gender: Optional. The SSML voice gender (e.g., texttospeech.SsmlVoiceGender.FEMALE).
    Returns:
        A VoiceSelectionParams object for use in synthesis requests.
    """
    voice_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=ssml_gender
    )
    return voice_params
