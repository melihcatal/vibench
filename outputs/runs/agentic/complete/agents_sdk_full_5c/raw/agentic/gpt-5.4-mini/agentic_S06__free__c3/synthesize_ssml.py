from __future__ import annotations

from speech_client import synthesize
from speech_models import SynthesisRequest


def synthesize_ssml(ssml: str, language_code: str = "en-US", voice_name: str | None = None, speaking_rate: float = 1.0, pitch: float = 0.0) -> bytes:
    request = SynthesisRequest(
        text=ssml,
        language_code=language_code,
        voice_name=voice_name,
        speaking_rate=speaking_rate,
        pitch=pitch,
        ssml=True,
    )
    return synthesize(request)
