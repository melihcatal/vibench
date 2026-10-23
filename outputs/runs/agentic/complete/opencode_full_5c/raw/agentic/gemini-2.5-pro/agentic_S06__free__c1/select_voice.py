from google.cloud import texttospeech
from speech_client import get_speech_client


def select_voice(language_code: str, name_filter: str = "Wavenet"):
    """Lists available voices for a language and returns the first match."""
    client = get_speech_client()

    voices = client.list_voices(language_code=language_code)

    for voice in voices.voices:
        if name_filter in voice.name:
            return {
                "name": voice.name,
                "ssml_gender": texttospeech.SsmlVoiceGender(voice.ssml_gender).name,
                "natural_sample_rate_hertz": voice.natural_sample_rate_hertz,
            }
    return None
