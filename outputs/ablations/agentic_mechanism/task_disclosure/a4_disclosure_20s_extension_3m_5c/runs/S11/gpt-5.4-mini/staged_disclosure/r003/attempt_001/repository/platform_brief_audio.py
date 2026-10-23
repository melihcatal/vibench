import base64
import json
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_TTS_MODEL = "gpt-4o-mini-tts"
OPENAI_TTS_URL = "https://api.openai.com/v1/audio/speech"


@dataclass
class BriefAudioResult:
    audio_bytes: bytes
    content_type: str


def _coerce_brief_text(platform_output: Any) -> str:
    if isinstance(platform_output, str):
        return platform_output.strip()
    if isinstance(platform_output, dict):
        for key in ("brief", "summary", "output", "text", "message"):
            value = platform_output.get(key)
            if isinstance(value, str) and value.strip():
                return value.strip()
        return json.dumps(platform_output, ensure_ascii=False, sort_keys=True)
    return str(platform_output).strip()


def generate_spoken_briefing(platform_output: Any, voice: str = "alloy", response_format: str = "mp3") -> BriefAudioResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")

    text = _coerce_brief_text(platform_output)
    if not text:
        raise ValueError("platform_output produced empty briefing text")

    payload: Dict[str, Any] = {
        "model": OPENAI_TTS_MODEL,
        "input": text,
        "voice": voice,
        "response_format": response_format,
    }

    response = requests.post(
        OPENAI_TTS_URL,
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json=payload,
        timeout=60,
    )
    response.raise_for_status()

    content_type = response.headers.get("Content-Type", f"audio/{response_format}")
    if "application/json" in content_type:
        data = response.json()
        audio_b64 = data.get("audio") or data.get("data")
        if isinstance(audio_b64, str):
            return BriefAudioResult(base64.b64decode(audio_b64), content_type)
        raise RuntimeError("Unexpected JSON response from OpenAI TTS API")

    return BriefAudioResult(response.content, content_type)


def save_briefing_audio(platform_output: Any, output_path: str, voice: str = "alloy", response_format: str = "mp3") -> str:
    result = generate_spoken_briefing(platform_output, voice=voice, response_format=response_format)
    with open(output_path, "wb") as f:
        f.write(result.audio_bytes)
    return output_path
