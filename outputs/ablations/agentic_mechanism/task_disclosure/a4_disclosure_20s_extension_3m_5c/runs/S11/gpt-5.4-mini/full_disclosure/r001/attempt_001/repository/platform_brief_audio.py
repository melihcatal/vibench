import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

from openai import OpenAI


@dataclass
class PlatformBriefAudioRequest:
    output_text: str
    voice: Optional[str] = None
    model: Optional[str] = None
    response_format: Optional[str] = None
    instructions: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


@dataclass
class PlatformBriefAudioResponse:
    audio: Any
    response: Any
    metadata: Dict[str, Any]


def _extract_text(output: Any) -> str:
    if output is None:
        return ""
    if isinstance(output, str):
        return output
    if isinstance(output, dict):
        for key in ("text", "output_text", "content", "message"):
            value = output.get(key)
            if isinstance(value, str):
                return value
        return str(output)
    return getattr(output, "text", None) or str(output)


def generate_platform_brief_audio(
    output: Any,
    *,
    voice: Optional[str] = None,
    model: Optional[str] = None,
    response_format: Optional[str] = None,
    instructions: Optional[str] = None,
    metadata: Optional[Dict[str, Any]] = None,
    api_key: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> PlatformBriefAudioResponse:
    text = _extract_text(output)
    resolved_client = client or OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))
    resolved_model = model or os.environ.get("OPENAI_TTS_MODEL", "gpt-4o-mini-tts")
    payload: Dict[str, Any] = {
        "model": resolved_model,
        "voice": voice or os.environ.get("OPENAI_TTS_VOICE", "alloy"),
        "input": text,
    }
    if response_format is not None:
        payload["response_format"] = response_format
    if instructions is not None:
        payload["instructions"] = instructions
    response = resolved_client.audio.speech.create(**payload)
    return PlatformBriefAudioResponse(
        audio=response,
        response=response,
        metadata={
            "provider": "openai",
            "model": resolved_model,
            "voice": payload["voice"],
            **(metadata or {}),
        },
    )
