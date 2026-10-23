from __future__ import annotations

from typing import Generator, Iterable

import pyaudio

from speech_client import (
    create_speech_client,
    load_stream_settings,
    start_streaming_recognition,
)
from speech_models import (
    StreamingTranscriptEvent,
    normalize_bytes_chunk,
    parse_google_streaming_response,
)


def microphone_audio_chunks(
    *,
    sample_rate_hz: int = 16000,
    chunk_size: int = 3200,
    channels: int = 1,
) -> Generator:
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=channels,
        rate=sample_rate_hz,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while True:
            yield normalize_bytes_chunk(
                stream.read(chunk_size, exception_on_overflow=False)
            )
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone_transcripts() -> Iterable[StreamingTranscriptEvent]:
    client = create_speech_client()
    settings = load_stream_settings()
    responses = start_streaming_recognition(client, settings, microphone_audio_chunks())
    for response in responses:
        for event in parse_google_streaming_response(response):
            yield event
