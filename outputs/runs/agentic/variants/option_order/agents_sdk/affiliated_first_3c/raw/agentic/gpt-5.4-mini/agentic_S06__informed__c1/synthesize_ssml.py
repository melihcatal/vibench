from __future__ import annotations

from speech_client import synthesize_text_request
from speech_models import TTSRequest, normalize_text


def synthesize_ssml(
    ssml: str,
    voice_name: str | None = None,
    locale: str | None = None,
    prosody_rate: str | None = None,
    prosody_pitch: str | None = None,
) -> bytes:
    ssml_text = normalize_text(ssml)
    response = synthesize_text_request(
        TTSRequest(
            text=ssml_text,
            voice_name=voice_name,
            locale=locale,
            ssml=True,
            extra={"prosody_rate": prosody_rate, "prosody_pitch": prosody_pitch},
        )
    )
    return response.audio
