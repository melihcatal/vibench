from __future__ import annotations

from speech_client import (
    get_tts_client,
    resolve_model_id,
    resolve_output_format,
    resolve_voice_id,
)
from speech_models import AudioResult, SynthesisRequest


def synthesize_text(request: SynthesisRequest) -> AudioResult:
    if not request.text:
        raise ValueError("request.text is required")
    client = get_tts_client()
    audio_iter = client.text_to_speech.convert(
        voice_id=resolve_voice_id(request.voice_id),
        model_id=resolve_model_id(),
        text=request.text,
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
        metadata={"model_id": resolve_model_id()},
    )
