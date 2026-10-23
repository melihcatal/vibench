from speech_client import SpeechClient
from speech_models import SpeechRequest, normalize_ssml


def synthesize_ssml(text: str, voice: str = None, locale: str = "en-US", rate: str = None, pitch: str = None) -> bytes:
    client = SpeechClient()
    ssml = normalize_ssml(text, voice=voice, rate=rate, pitch=pitch)
    response = client.synthesize(SpeechRequest(text=ssml, voice=voice, locale=locale, ssml=True))
    return response.audio
