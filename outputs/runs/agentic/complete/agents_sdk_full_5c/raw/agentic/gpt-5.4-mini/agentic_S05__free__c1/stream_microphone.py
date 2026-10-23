from __future__ import annotations

import queue
from typing import Generator, Iterable

import pyaudio
from google.cloud import speech

from speech_client import create_speech_client, load_config, streaming_config


RATE = 16000
CHUNK = int(RATE / 10)


def microphone_audio_stream() -> Generator[bytes, None, None]:
    q: queue.Queue[bytes] = queue.Queue()

    def callback(in_data, frame_count, time_info, status):
        q.put(in_data)
        return None, pyaudio.paContinue

    audio = pyaudio.PyAudio()
    stream = audio.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=RATE,
        input=True,
        frames_per_buffer=CHUNK,
        stream_callback=callback,
    )
    stream.start_stream()
    try:
        while True:
            yield q.get()
    finally:
        stream.stop_stream()
        stream.close()
        audio.terminate()


def stream_microphone() -> Iterable[str]:
    client = create_speech_client()
    cfg = load_config()
    requests = (speech.StreamingRecognizeRequest(audio_content=chunk) for chunk in microphone_audio_stream())
    responses = client.streaming_recognize(streaming_config(cfg), requests)
    for response in responses:
        for result in response.results:
            if result.alternatives:
                yield result.alternatives[0].transcript
