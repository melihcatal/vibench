from __future__ import annotations

from speech_client import GoogleSpeechClient
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_text(
    text: str,
    *,
    voice_name: str = "en-US-Neural2-F",
    language_code: str = "en-US",
    audio_encoding: str = "MP3",
) -> bytes:
    client = GoogleSpeechClient()
    request = SynthesisRequest(
        text=text,
        voice_name=voice_name,
        language_code=language_code,
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
