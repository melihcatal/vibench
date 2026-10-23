from __future__ import annotations

import io
from typing import Iterator

from dashscope.audio.asr import Recognition

from speech_client import SpeechClientConfig, StreamingSpeechClient
from speech_models import NormalizedTranscriptEvent


def stream_microphone(audio_stream: io.BufferedIOBase, config: SpeechClientConfig | None = None) -> Iterator[NormalizedTranscriptEvent]:
    client = StreamingSpeechClient(config)
    recognizer: Recognition = client.start_recognizer()
    recognizer.start()
    while True:
        chunk = audio_stream.read(3200)
        if not chunk:
            break
        recognizer.send(chunk)
        for event in getattr(client, "events", []):
            yield event
    recognizer.stop()


def iter_microphone_transcripts(audio_stream: io.BufferedIOBase) -> Iterator[str]:
    for event in stream_microphone(audio_stream):
        if event.text:
            yield event.text
