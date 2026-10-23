from __future__ import annotations

from speech_client import OPENAI_BASE_URL, build_json_headers, request_json
from speech_models import SynthesisResponse


def synthesize_ssml(
    ssml: str, voice: str = "alloy", model: str = "gpt-4o-mini-tts"
) -> SynthesisResponse:
    instructions = f"Render this SSML faithfully, preserving prosody and emphasis controls where possible: {ssml}"
    payload = {
        "model": model,
        "voice": voice,
        "input": instructions,
        "format": "mp3",
    }
    response = request_json(
        "POST",
        f"{OPENAI_BASE_URL}/audio/speech",
        headers=build_json_headers("openai"),
        json=payload,
    )
    audio_hex = response.get("data") or response.get("audio") or ""
    audio_bytes = bytes.fromhex(audio_hex) if audio_hex else b""
    return SynthesisResponse(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        provider="openai",
        voice=voice,
        request_id=response.get("id"),
    )
