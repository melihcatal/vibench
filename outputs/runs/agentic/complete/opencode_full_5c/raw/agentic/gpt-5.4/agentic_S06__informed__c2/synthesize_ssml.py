from __future__ import annotations

from speech_client import (
    DEFAULT_OUTPUT_FORMAT,
    DEFAULT_TTS_MODEL,
    get_default_voice_id,
    get_elevenlabs_client,
)
from speech_models import AudioArtifact, SsmlSynthesisRequest


def synthesize_ssml(request: SsmlSynthesisRequest) -> AudioArtifact:
    client = get_elevenlabs_client()
    voice_id = get_default_voice_id(request.voice_id)
    audio = client.text_to_speech.convert(
        voice_id=voice_id,
        model_id=request.model_id or DEFAULT_TTS_MODEL,
        output_format=request.output_format or DEFAULT_OUTPUT_FORMAT,
        text=request.ssml,
    )
    audio_bytes = b"".join(audio)
    return AudioArtifact(
        audio_bytes=audio_bytes,
        voice_id=voice_id,
        model_id=request.model_id or DEFAULT_TTS_MODEL,
    )
