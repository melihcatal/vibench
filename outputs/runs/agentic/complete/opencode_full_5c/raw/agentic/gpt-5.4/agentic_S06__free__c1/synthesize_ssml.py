from __future__ import annotations

from typing import Optional

from speech_client import get_openai_client, resolve_tts_model
from speech_models import SpeechSynthesisRequest, SpeechSynthesisResult


def synthesize_ssml(
    ssml: str,
    voice: str = "alloy",
    audio_format: str = "mp3",
    model: Optional[str] = None,
    speed: float = 1.0,
    api_key: Optional[str] = None,
) -> SpeechSynthesisResult:
    request = SpeechSynthesisRequest(
        ssml=ssml,
        voice=voice,
        model=resolve_tts_model(model),
        audio_format=audio_format,
        speed=speed,
    )
    client = get_openai_client(api_key)
    response = client.audio.speech.create(**request.to_openai_payload())
    return SpeechSynthesisResult(
        audio_bytes=response.read(),
        model=request.model,
        voice=request.voice,
        audio_format=request.audio_format,
    )
