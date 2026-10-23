from __future__ import annotations

from typing import Optional
from xml.sax.saxutils import escape

from speech_client import build_session
from speech_models import TTSResponse


DEFAULT_VOICE_ID = "EXAVITQu4vr4xnSDxMaL"


def _render_ssml(text: str, rate: str = "100%", pitch: str = "0%", volume: str = "+0dB") -> str:
    escaped = escape(text)
    return (
        "<speak>"
        f"<prosody rate=\"{rate}\" pitch=\"{pitch}\" volume=\"{volume}\">"
        f"{escaped}"
        "</prosody>"
        "</speak>"
    )


def synthesize_ssml(
    text: str,
    voice_id: str = DEFAULT_VOICE_ID,
    model_id: Optional[str] = None,
    rate: str = "95%",
    pitch: str = "+2%",
    volume: str = "+0dB",
) -> TTSResponse:
    session, config = build_session()
    model = model_id or config.default_model
    url = f"{config.base_url}/text-to-speech/{voice_id}"
    payload = {
        "text": _render_ssml(text=text, rate=rate, pitch=pitch, volume=volume),
        "model_id": model,
        "output_format": config.default_output_format,
        "apply_text_normalization": "auto",
    }
    response = session.post(url, json=payload, timeout=config.timeout)
    response.raise_for_status()
    return TTSResponse(
        audio_bytes=response.content,
        content_type=response.headers.get("Content-Type", "audio/mpeg"),
        voice_id=voice_id,
        model_id=model,
    )
