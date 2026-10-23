from __future__ import annotations

from speech_client import (
    ELEVENLABS_BASE_URL,
    build_elevenlabs_headers,
    build_tts_payload,
    request_bytes,
)
from speech_models import SynthesisRequest, SynthesisResponse


def synthesize_text(request: SynthesisRequest) -> SynthesisResponse:
    voice_id = request.voice or "21m00Tcm4TlvDq8ikWAM"
    payload = build_tts_payload(
        text=request.text,
        voice_id=voice_id,
        audio_format=request.audio_format,
        speaking_rate=request.speaking_rate,
        pitch=request.pitch,
    )
    response = request_bytes(
        "POST",
        f"{ELEVENLABS_BASE_URL}/v1/text-to-speech/{voice_id}",
        headers=build_elevenlabs_headers(),
        json=payload,
    )
    return SynthesisResponse(
        audio_bytes=response.content,
        content_type=response.headers.get("Content-Type", "audio/mpeg"),
        provider="elevenlabs",
        voice=voice_id,
        request_id=response.headers.get("request-id"),
    )
