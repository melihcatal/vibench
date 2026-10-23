from google.cloud import texttospeech
from speech_client import get_tts_client
from google.cloud.texttospeech_v1.types import ListVoicesResponse

def list_voices_for_locale(language_code: str):
    client = get_tts_client()
    response: ListVoicesResponse = client.list_voices(language_code=language_code)
    return [{"name": voice.name, "gender": voice.gender.name, "language_codes": voice.language_codes} for voice in response.voices]

def select_voice(language_code: str, preferred_gender: str = "FEMALE"):
    voices = list_voices_for_locale(language_code)
    for voice in voices:
        if preferred_gender.lower() in voice["gender"].lower():
            return voice["name"]
    return voices[0]["name"] if voices else None
