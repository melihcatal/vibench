from __future__ import annotations

from typing import Any

from speech_client import OPENAI_TRANSCRIBE_MODEL, realtime_session_config
from speech_models import StreamingConfig


async def configure_streaming_session(
    connection: Any,
    language_code: str = "en-US",
    punctuate: bool = True,
    sample_rate_hz: int = 16000,
) -> None:
    config = StreamingConfig(
        language_code=language_code,
        punctuate=punctuate,
        sample_rate_hz=sample_rate_hz,
    )
    payload = realtime_session_config(config)
    payload["session"]["input_audio_transcription"]["model"] = OPENAI_TRANSCRIBE_MODEL
    await connection.send(payload)
