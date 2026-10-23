from __future__ import annotations

from speech_client import GoogleSpeechClient
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_ssml(
    ssml: str,
    *,
    voice_name: str = "en-US-Studio-O",
    language_code: str = "en-US",
    speaking_rate: float = 0.95,
    pitch: float = -2.0,
    audio_encoding: str = "MP3",
) -> bytes:
    client = GoogleSpeechClient()
    request = SynthesisRequest(
        ssml=ssml,
        voice_name=voice_name,
        language_code=language_code,
        speaking_rate=speaking_rate,
        pitch=pitch,
        audio_encoding=audio_encoding,
    )
    payload = {
        "input": request.to_google_input(),
        "voice": request.to_google_voice(),
        "audioConfig": request.to_google_audio_config(),
    }
    response = client.synthesize(payload)
    normalized = SynthesisResponse.from_google_response(
        response,
        voice_name=voice_name,
        audio_encoding=audio_encoding,
    )
    return normalized.audio_content
