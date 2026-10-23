from __future__ import annotations

import os
from typing import Optional

from openai import AsyncOpenAI

from speech_models import StreamingConfig


OPENAI_REALTIME_MODEL = os.getenv("OPENAI_REALTIME_MODEL", "gpt-4o-realtime-preview")
OPENAI_TRANSCRIBE_MODEL = os.getenv("OPENAI_TRANSCRIBE_MODEL", "gpt-4o-mini-transcribe")


def get_openai_client(api_key: Optional[str] = None) -> AsyncOpenAI:
    return AsyncOpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY"))


def realtime_session_config(config: Optional[StreamingConfig] = None) -> dict:
    cfg = config or StreamingConfig()
    return {
        "type": "transcription_session.update",
        "session": {
            "input_audio_format": "pcm16",
            "input_audio_transcription": {
                "model": OPENAI_TRANSCRIBE_MODEL,
                "language": cfg.language_code,
                "prompt": "Return readable streaming captions with punctuation." if cfg.punctuate else "Return verbatim streaming transcript.",
            },
            "turn_detection": {
                "type": "server_vad",
                "threshold": 0.5,
                "prefix_padding_ms": 250,
                "silence_duration_ms": 500,
            },
        },
    }


def pcm16_bytes_to_base64(audio: bytes) -> str:
    import base64

    return base64.b64encode(audio).decode("ascii")
