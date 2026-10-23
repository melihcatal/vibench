from __future__ import annotations

from typing import Optional

from speech_client import ElevenLabsConfig, build_session
from speech_models import TTSRequest, TTSResponse


DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"


def synthesize_text(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: Optional[str] = None,
    output_format: Optional[str] = None,
    stability: float = 0.5,
    similarity_boost: float = 0.75,
) -> TTSResponse:
    request = TTSRequest(text=text, voice_id=voice_id)
    session, config = build_session()
    model = model_id or config.default_model
    fmt = output_format or config.default_output_format
    url = f"{config.base_url}/text-to-speech/{voice_id}"
    payload = {
        **request.as_text_payload(),
        "model_id": model,
        "output_format": fmt,
        "voice_settings": {
            "stability": stability,
            "similarity_boost": similarity_boost,
        },
    }
    response = session.post(url, json=payload, timeout=config.timeout)
    response.raise_for_status()
    return TTSResponse(
        audio_bytes=response.content,
        content_type=response.headers.get("Content-Type", "audio/mpeg"),
        voice_id=voice_id,
        model_id=model,
    )
