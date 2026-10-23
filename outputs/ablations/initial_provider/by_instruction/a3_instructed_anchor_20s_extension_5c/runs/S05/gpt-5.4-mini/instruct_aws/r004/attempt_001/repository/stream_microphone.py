import os
from typing import Iterable, Iterator

import pyaudio

from speech_client import load_speech_config, stream_transcribe
from speech_models import StreamingAudioChunk, TranscriptSegment


def microphone_audio_chunks(sample_rate_hz: int, chunk_size: int = 1024) -> Iterator[StreamingAudioChunk]:
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=sample_rate_hz, input=True, frames_per_buffer=chunk_size)
    try:
        while True:
            yield StreamingAudioChunk(payload=stream.read(chunk_size, exception_on_overflow=False), sample_rate_hz=sample_rate_hz)
    finally:
        stream.stop_stream()
        stream.close()
        pa.terminate()


def stream_microphone() -> Iterator[str]:
    config = load_speech_config()
    for segment in stream_transcribe(microphone_audio_chunks(config.sample_rate_hz), language_code=config.language_code, enable_punctuation=config.enable_punctuation):
        if segment.text:
            yield segment.text


def collect_interim_transcripts(limit: int = 0) -> Iterable[TranscriptSegment]:
    count = 0
    for text in stream_microphone():
        count += 1
        yield TranscriptSegment(text=text, is_final=False)
        if limit and count >= limit:
            break
