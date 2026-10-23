from __future__ import annotations

from xml.etree import ElementTree as ET

from speech_client import (
    get_tts_client,
    resolve_model_id,
    resolve_output_format,
    resolve_voice_id,
)
from speech_models import AudioResult, SynthesisRequest


def _ssml_to_text(ssml: str) -> str:
    root = ET.fromstring(ssml)
    return " ".join(part.strip() for part in root.itertext() if part and part.strip())


def synthesize_ssml(request: SynthesisRequest) -> AudioResult:
    if not request.ssml:
        raise ValueError("request.ssml is required")
    client = get_tts_client()
    text = _ssml_to_text(request.ssml)
    audio_iter = client.text_to_speech.convert(
        voice_id=resolve_voice_id(request.voice_id),
        model_id=resolve_model_id(),
        text=text,
        output_format=resolve_output_format(request.output_format),
    )
    audio_bytes = b"".join(
        chunk for chunk in audio_iter if isinstance(chunk, (bytes, bytearray))
    )
    return AudioResult(
        audio_bytes=audio_bytes,
        content_type="audio/mpeg",
        provider="elevenlabs",
        voice_id=resolve_voice_id(request.voice_id),
        metadata={
            "model_id": resolve_model_id(),
            "source_format": "ssml",
            "prosody_requested": any(
                tag in request.ssml for tag in ("prosody", "voice", "break")
            ),
        },
    )
