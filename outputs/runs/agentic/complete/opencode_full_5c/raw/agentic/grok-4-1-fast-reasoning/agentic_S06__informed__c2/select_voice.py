from speech_client import get_polly_client
from speech_models import VoiceInfo


def list_voices(locale: str = "en-US") -> list[VoiceInfo]:
    client = get_polly_client()
    response = client.describe_voices(LanguageCode=locale)
    return response["Voices"]


def select_voice(locale: str = "en-US", gender: str = "Female") -> str:
    voices = list_voices(locale)
    for voice in voices:
        if voice.get("Gender") == gender:
            return voice["Id"]
    return voices[0]["Id"] if voices else "Joanna"
