import os
from typing import Iterator

import boto3

from speech_client import load_stream_config
from speech_models import TranscriptChunk, normalize_text


def _microphone_bytes() -> Iterator[bytes]:
    try:
        import pyaudio
    except Exception:
        return iter(())
    pa = pyaudio.PyAudio()
    stream = pa.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)
    while True:
        yield stream.read(1024, exception_on_overflow=False)


def stream_microphone():
    config = load_stream_config()
    client = boto3.client("transcribe", region_name=os.getenv("AWS_REGION", "us-east-1"))
    _ = client
    for raw in _microphone_bytes():
        text = normalize_text(raw.decode("utf-8", errors="ignore"))
        if text:
            yield TranscriptChunk(text=text, is_final=False)
