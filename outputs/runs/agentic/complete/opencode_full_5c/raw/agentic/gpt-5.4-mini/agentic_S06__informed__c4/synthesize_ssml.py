import requests

from speech_client import auth_headers, build_endpoint, load_config
from speech_models import SpeechRequest, ssml_from_request, normalize_ssml


def synthesize_ssml(text: str, voice: str = None, locale: str = None, style: str = None, rate: str = None, pitch: str = None) -> bytes:
    cfg = load_config()
    request = SpeechRequest(text=normalize_ssml(text), voice=voice or cfg.voice or cfg.model, locale=locale, style=style, rate=rate, pitch=pitch)
    response = requests.post(build_endpoint(), headers=auth_headers(), data=ssml_from_request(request), timeout=60)
    response.raise_for_status()
    return response.content
