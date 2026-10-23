from __future__ import annotations

import base64
import os
from dataclasses import dataclass
from typing import Any, Dict, Optional

import requests


OPENAI_TRANSCRIBE_URL = "https://api.openai.com/v1/audio/transcriptions"
OPENAI_MODEL = "whisper-1"


@dataclass
class TTSQATranscriptResult:
    text: str
    raw: Dict[str, Any]


def _audio_payload(audio: bytes) -> bytes:
    return audio if isinstance(audio, (bytes, bytearray)) else bytes(audio)


def transcribe_tts_qa_sample(audio: bytes, filename: str = "sample.wav", language: Optional[str] = None) -> TTSQATranscriptResult:
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    files = {
        "file": (filename, _audio_payload(audio)),
    }
    data: Dict[str, Any] = {"model": OPENAI_MODEL}
    if language:
        data["language"] = language
    response = requests.post(
        OPENAI_TRANSCRIBE_URL,
        headers={"Authorization": f"Bearer {api_key}"},
        files=files,
        data=data,
        timeout=120,
    )
    response.raise_for_status()
    payload = response.json()
    return TTSQATranscriptResult(text=payload.get("text", ""), raw=payload)


def transcribe_tts_qa_sample_base64(audio_b64: str, filename: str = "sample.wav", language: Optional[str] = None) -> TTSQATranscriptResult:
    return transcribe_tts_qa_sample(base64.b64decode(audio_b64), filename=filename, language=language)
