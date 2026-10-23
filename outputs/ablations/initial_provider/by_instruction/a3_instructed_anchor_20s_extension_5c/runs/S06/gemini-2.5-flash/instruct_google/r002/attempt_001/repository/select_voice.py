from google.cloud import texttospeech
from speech_client import get_tts_client

def list_voices(language_code: str = None):
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices
    return voices

def select_voice_by_criteria(
    language_code: str = "en-US",
    name_substring: str = None,
    ssml_gender: texttospeech.SsmlVoiceGender = None
):
    client = get_tts_client()
    voices = client.list_voices(language_code=language_code).voices

    filtered_voices = []
    for voice in voices:
        match = True
        if name_substring and name_substring.lower() not in voice.name.lower():
            match = False
        if ssml_gender and voice.ssml_gender != ssml_gender:
            match = False
        if match:
            filtered_voices.append(voice)
    return filtered_voices
