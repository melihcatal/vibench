from __future__ import annotations

from speech_client import synthesize_text as azure_synthesize_text
from speech_models import TTSRequest, TTSResponse, build_ssml


def synthesize_ssml(text: str, voice: str, locale: str | None = None, prosody_rate: str | None = None, prosody_pitch: str | None = None) -> TTSResponse:
    _ = build_ssml(text, voice=voice, rate=prosody_rate, pitch=prosody_pitch, locale=locale)
    request = TTSRequest(text=text, voice=voice, locale=locale, format="mp3", ssml=True, prosody_rate=prosody_rate, prosody_pitch=prosody_pitch)
    audio = azure_synthesize_text(request)
    return TTSResponse(audio=audio, content_type="audio/mpeg", provider="azure", voice=voice)
