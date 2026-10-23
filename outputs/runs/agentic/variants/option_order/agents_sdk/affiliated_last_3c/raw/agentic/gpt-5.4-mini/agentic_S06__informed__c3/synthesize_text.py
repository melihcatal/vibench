from __future__ import annotations

from speech_client import synthesize_text as azure_synthesize_text
from speech_models import TTSRequest, TTSResponse


def synthesize_text(text: str, voice: str | None = None, locale: str | None = None, format: str = "mp3") -> TTSResponse:
    request = TTSRequest(text=text, voice=voice, locale=locale, format=format, ssml=False)
    audio = azure_synthesize_text(request)
    return TTSResponse(audio=audio, content_type="audio/mpeg", provider="azure", voice=voice)
