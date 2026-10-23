from __future__ import annotations

from typing import Iterable

import pyaudio

from google.cloud import speech

from speech_client import SpeechClientHelper
from speech_models import AudioChunk, TranscriptSegment


def microphone_audio_chunks(sample_rate_hz: int = 16000, chunk_size: int = 1600) -> Iterable[AudioChunk]:
    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=sample_rate_hz,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while True:
            yield AudioChunk(data=stream.read(chunk_size, exception_on_overflow=False), sample_rate_hz=sample_rate_hz)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone(language_code: str = "en-US") -> Iterable[TranscriptSegment]:
    helper = SpeechClientHelper()
    responses = helper.stream_audio(microphone_audio_chunks(helper.config.sample_rate_hz), language_code=language_code)
    for response in responses:
        for segment in helper.response_to_segments(response):
            if segment.text:
                yield segment
