import os
from speech_client import get_texttospeech_client

def synthesize_ssml(ssml: str, voice: str = None, locale: str = None) -> bytes:
    """Synthesize SSML with voice and prosody controls using IBM Watson TTS.
    The SSML string must be well‑formed and escaped where necessary.
    """
    client = get_texttospeech_client()
    params = {
        "text": ssml,
        "accept": "audio/wav",
        "content_type": "application/ssml+xml",
    }
    if voice:
        params["voice"] = voice
    if locale:
        params["language"] = locale
    result = client.synthesize_speech(**params)
    return result.get_result().content
