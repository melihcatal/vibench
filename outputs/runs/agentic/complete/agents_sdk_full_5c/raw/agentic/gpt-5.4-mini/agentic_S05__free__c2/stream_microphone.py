from __future__ import annotations

import queue
from typing import Iterator

import pyaudio
from google.cloud import speech_v1p1beta1 as speech

from speech_client import SpeechConfig, build_streaming_config, get_speech_client

CHUNK = 1600
RATE = 16000


class MicrophoneStream:
    def __init__(self, rate: int = RATE, chunk: int = CHUNK) -> None:
        self._rate = rate
        self._chunk = chunk
        self._buff: queue.Queue[bytes | None] = queue.Queue()
        self._audio_interface = pyaudio.PyAudio()
        self._audio_stream = None

    def __enter__(self) -> "MicrophoneStream":
        self._audio_stream = self._audio_interface.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self._rate,
            input=True,
            frames_per_buffer=self._chunk,
            stream_callback=self._fill_buffer,
        )
        self._audio_stream.start_stream()
        return self

    def __exit__(self, exc_type, exc, tb) -> None:
        if self._audio_stream is not None:
            self._audio_stream.stop_stream()
            self._audio_stream.close()
        self._audio_interface.terminate()
        self._buff.put(None)

    def _fill_buffer(self, in_data, frame_count, time_info, status_flags):
        self._buff.put(in_data)
        return None, pyaudio.paContinue

    def generator(self) -> Iterator[bytes]:
        while True:
            chunk = self._buff.get()
            if chunk is None:
                return
            yield chunk


def stream_microphone() -> Iterator[str]:
    client = get_speech_client()
    config = build_streaming_config(SpeechConfig())

    with MicrophoneStream() as mic:
        requests = (speech.StreamingRecognizeRequest(audio_content=content) for content in mic.generator())
        responses = client.streaming_recognize(config=config, requests=requests)
        for response in responses:
            for result in response.results:
                if result.alternatives:
                    yield result.alternatives[0].transcript
