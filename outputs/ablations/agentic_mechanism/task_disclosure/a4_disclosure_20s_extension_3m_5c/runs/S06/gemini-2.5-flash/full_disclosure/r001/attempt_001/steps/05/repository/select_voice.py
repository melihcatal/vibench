from google.cloud import texttospeech

def list_voices():
    """Lists the available voices."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices().voices

    for voice in voices:
        print(f"Name: {voice.name}")
        print(f"  SSML Gender: {texttospeech.SsmlVoiceGender(voice.ssml_gender).name}")
        print(f"  Natural Sample Rate Hertz: {voice.natural_sample_rate_hertz}")
        print(f"  Supported language codes: {voice.language_codes}")

def select_voice(language_code: str, name: str = None, ssml_gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL):
    """Selects a voice based on language code, name, and SSML gender."""
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices

    if name:
        for voice in voices:
            if voice.name == name:
                return voice
    else:
        for voice in voices:
            if voice.ssml_gender == ssml_gender:
                return voice
    return None
