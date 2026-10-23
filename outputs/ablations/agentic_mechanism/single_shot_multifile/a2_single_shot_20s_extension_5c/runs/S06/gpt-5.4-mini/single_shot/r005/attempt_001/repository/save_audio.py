from __future__ import annotations

from pathlib import Path
from typing import BinaryIO

from speech_client import get_tts_client
from speech_models import AudioSaveRequest, AudioSaveResponse, TextToSpeechResponse


def save_audio(speech: TextToSpeechResponse, output_path: str | Path | None = None, stream: BinaryIO | None = None) -> AudioSaveResponse:
    client = get_tts_client()
    request = AudioSaveRequest(audio_bytes=speech.audio_bytes, output_path=output_path, stream=stream, content_type=speech.content_type)
    return client.save_audio(request)
