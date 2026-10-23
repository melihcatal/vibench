import queue
from typing import Iterator

import pyaudio
from google.cloud import speech

from speech_client import build_streaming_config, create_client, load_config
from speech_models import SpeechChunk, TranscriptionRequest, TranscriptEvent


def audio_chunks(
    stream: pyaudio.Stream, chunk_size: int = 1600
) -> Iterator[SpeechChunk]:
    while True:
        data = stream.read(chunk_size, exception_on_overflow=False)
        if not data:
            break
        yield SpeechChunk(audio=data)


def stream_microphone() -> Iterator[TranscriptEvent]:
    cfg = load_config()
    client = create_client()
    request = TranscriptionRequest(
        language_code=cfg.language_code, enable_punctuation=cfg.enable_punctuation
    )
    recognizer = build_streaming_config(request)
    mic = pyaudio.PyAudio()
    stream = mic.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1600,
    )
    try:
        requests = (
            speech.StreamingRecognizeRequest(audio_content=chunk.audio)
            for chunk in audio_chunks(stream)
        )
        for response in client.streaming_recognize(recognizer, requests):
            for result in response.results:
                if result.alternatives:
                    yield TranscriptEvent(
                        text=result.alternatives[0].transcript, is_final=result.is_final
                    )
    finally:
        stream.stop_stream()
        stream.close()
        mic.terminate()
