import os
from google.cloud import texttospeech

def list_voices(language_code: str = ""):
    """Lists the available voices for a given language code.

    Args:
        language_code: The BCP-47 language tag to query for voices.
    """
    client = texttospeech.TextToSpeechClient()
    voices = client.list_voices(language_code=language_code).voices
    return voices

def select_voice(language_code: str, ssml_gender: texttospeech.SsmlVoiceGender = texttospeech.SsmlVoiceGender.NEUTRAL):
    """Selects a voice based on language code and SSML gender.

    Args:
        language_code: The BCP-47 language tag.
        ssml_gender: The SSML voice gender.
    """
    client = texttospeech.TextToSpeechClient()
    voice_selection_params = texttospeech.VoiceSelectionParams(
        language_code=language_code,
        ssml_gender=ssml_gender
    )
    return voice_selection_params
