from __future__ import annotations

from speech_client import synthesize
from speech_models import SynthesisRequest


def synthesize_text(text: str, language_code: str = "en-US", voice_name: str | None = None) -> bytes:
    request = SynthesisRequest(text=text, language_code=language_code, voice_name=voice_name, ssml=False)
    return synthesize(request)
