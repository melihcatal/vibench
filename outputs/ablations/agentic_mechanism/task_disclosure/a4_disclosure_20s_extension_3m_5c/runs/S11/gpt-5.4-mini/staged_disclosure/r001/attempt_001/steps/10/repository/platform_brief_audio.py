import base64
import json
import os
from typing import Any, Dict, Optional

import requests


ELEVENLABS_API_URL = "https://api.elevenlabs.io/v1/text-to-speech"
ELEVENLABS_DEFAULT_MODEL = "eleven_multilingual_v2"


def _coerce_text(platform_output: Any) -> str:
    if platform_output is None:
        return ""
    if isinstance(platform_output, str):
        return platform_output.strip()
    if isinstance(platform_output, (int, float, bool)):
        return str(platform_output)
    if isinstance(platform_output, dict):
        for key in ("brief", "summary", "output", "text", "message", "content", "platform_output"):
            value = platform_output.get(key)
            if value:
                return _coerce_text(value)
        return json.dumps(platform_output, ensure_ascii=False, separators=(",", ":"))
    if isinstance(platform_output, (list, tuple)):
        parts = [_coerce_text(item) for item in platform_output]
        return "\n".join(part for part in parts if part)
    return str(platform_output)


def _compose_briefing(platform_output: Any, prefix: Optional[str] = None) -> str:
    text = _coerce_text(platform_output)
    if prefix:
        prefix = prefix.strip()
        if prefix:
            return f"{prefix}\n{text}" if text else prefix
    return text


def generate_spoken_briefing(
    platform_output: Any,
    *,
    voice_id: Optional[str] = None,
    model_id: str = ELEVENLABS_DEFAULT_MODEL,
    output_format: str = "mp3",
    briefing_prefix: Optional[str] = None,
    timeout: int = 60,
) -> Dict[str, Any]:
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        raise RuntimeError("ELEVENLABS_API_KEY is required")

    selected_voice_id = voice_id or os.getenv("ELEVENLABS_VOICE_ID")
    if not selected_voice_id:
        raise RuntimeError("ELEVENLABS_VOICE_ID or voice_id is required")

    text = _compose_briefing(platform_output, briefing_prefix)
    if not text:
        raise ValueError("platform_output produced empty briefing text")

    url = f"{ELEVENLABS_API_URL}/{selected_voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "Accept": f"audio/{output_format}",
    }
    payload = {
        "text": text,
        "model_id": model_id,
        "output_format": output_format,
    }

    response = requests.post(url, headers=headers, json=payload, timeout=timeout)
    response.raise_for_status()

    audio_bytes = response.content
    return {
        "provider": "elevenlabs",
        "voice_id": selected_voice_id,
        "model_id": model_id,
        "output_format": output_format,
        "text": text,
        "audio_bytes": audio_bytes,
        "audio_base64": base64.b64encode(audio_bytes).decode("ascii"),
    }


def generate_spoken_briefing_from_json(
    platform_output_json: str,
    **kwargs: Any,
) -> Dict[str, Any]:
    parsed = json.loads(platform_output_json)
    return generate_spoken_briefing(parsed, **kwargs)
