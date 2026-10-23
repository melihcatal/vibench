from __future__ import annotations

from google.cloud import texttospeech

from speech_client import get_google_tts_client
from speech_models import TTSRequest, TTSResponse


def synthesize_ssml(ssml: str, request: TTSRequest) -> TTSResponse:
    client = get_google_tts_client()
    synthesis_input = texttospeech.SynthesisInput(ssml=ssml)
    voice = client.build_voice_params(request.language_code, request.voice_name)
    audio_config = client.build_audio_config(
        audio_encoding=request.audio_encoding,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
        sample_rate_hertz=request.sample_rate_hz,
    )
    response = client.client.synthesize_speech(
        input=synthesis_input,
        voice=voice,
        audio_config=audio_config,
    )
    return TTSResponse(
        audio_bytes=response.audio_content,
        provider=client.provider,
        voice_name=request.voice_name,
        audio_encoding=request.audio_encoding,
        metadata={"input_type": "ssml", "language_code": request.language_code},
    )
