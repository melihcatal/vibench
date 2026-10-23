import os
from typing import Iterator

import pyaudio
from google.cloud import speech_v1 as speech

from speech_client import (
    build_recognition_config,
    create_speech_client,
    load_speech_config,
)
from speech_models import response_to_chunks


def microphone_audio_stream(chunk_size: int = 1600) -> Iterator[bytes]:
    audio = pyaudio.PyAudio()
    cfg = load_speech_config()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=cfg.sample_rate_hz,
        input=True,
        frames_per_buffer=chunk_size,
    )
    try:
        while True:
            yield stream.read(chunk_size, exception_on_overflow=False)
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone() -> Iterator[str]:
    client = create_speech_client()
    cfg = load_speech_config()
    recognition_config = build_recognition_config(cfg)
    streaming_config = speech.StreamingRecognitionConfig(
        config=recognition_config,
        interim_results=True,
        single_utterance=False,
    )
    requests = (
        speech.StreamingRecognizeRequest(audio_content=chunk)
        for chunk in microphone_audio_stream()
    )
    for response in client.streaming_recognize(streaming_config, requests):
        for chunk in response_to_chunks(response):
            if chunk.text:
                yield chunk.text
