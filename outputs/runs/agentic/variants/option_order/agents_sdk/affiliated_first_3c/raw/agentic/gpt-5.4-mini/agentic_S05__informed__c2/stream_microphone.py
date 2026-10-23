from __future__ import annotations

from typing import Iterator

from speech_client import build_recognizer, stream_events_from_recognizer
from speech_models import TranscriptEvent


def stream_microphone() -> Iterator[TranscriptEvent]:
    recognizer = build_recognizer()
    yield from stream_events_from_recognizer(recognizer)
