from speech_client import get_text_to_speech_client
from google.cloud import texttospeech


def list_voices(language_code: str = None):
    """
    Lists available voices for a target locale using Google Cloud Text-to-Speech.
    If language_code is None, lists all supported voices.
    """
    client = get_text_to_speech_client()
    response = client.list_voices(language_code=language_code)
    return response.voices


def select_voice_by_locale(
    language_code: str, ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
):
    """
    Selects a voice for a target locale using Google Cloud Text-to-Speech.
    Returns the first voice found for the given language code and gender.
    """
    voices = list_voices(language_code=language_code)
    for voice in voices:
        if voice.ssml_gender == ssml_gender:
            return voice
    return None
