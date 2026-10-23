from __future__ import annotations

from typing import Generator, Iterable

import pyaudio

from speech_client import get_google_speech_client, request_iter_from_chunks
from speech_models import (
    StreamingAudioChunk,
    StreamingSessionConfig,
    transcript_events_from_google,
)


def microphone_audio_chunks(
    sample_rate_hz: int = 16000, frames_per_buffer: int = 3200
) -> Generator[StreamingAudioChunk, None, None]:
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate_hz,
        input=True,
        frames_per_buffer=frames_per_buffer,
    )
    try:
        while True:
            yield StreamingAudioChunk(
                content=stream.read(frames_per_buffer, exception_on_overflow=False)
            )
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone_transcripts(
    config: StreamingSessionConfig | None = None,
) -> Iterable[str]:
    session = config or StreamingSessionConfig()
    client = get_google_speech_client()
    responses = client.streaming_recognize(
        requests=request_iter_from_chunks(
            microphone_audio_chunks(session.sample_rate_hz), session
        )
    )
    for response in responses:
        for event in transcript_events_from_google(response):
            if event.text:
                yield event.text
