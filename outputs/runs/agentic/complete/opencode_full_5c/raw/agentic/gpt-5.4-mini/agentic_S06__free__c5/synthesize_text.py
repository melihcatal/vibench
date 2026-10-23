from speech_client import SpeechClient
from speech_models import SpeechRequest


def synthesize_text(text: str, voice: str = None, locale: str = "en-US") -> bytes:
    client = SpeechClient()
    response = client.synthesize(SpeechRequest(text=text, voice=voice, locale=locale, ssml=False))
    return response.audio
