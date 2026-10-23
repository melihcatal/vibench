import json
import os
import queue
import sys
from typing import Iterator, Optional

import pyaudio
from openai import OpenAI


class MicrophoneTranscriptStreamer:
    def __init__(self, model: str = "gpt-4o-mini-transcribe", sample_rate: int = 16000):
        self.client = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        self.model = model
        self.sample_rate = sample_rate
        self._audio_queue: "queue.Queue[Optional[bytes]]" = queue.Queue()

    def _audio_source(self) -> Iterator[bytes]:
        while True:
            chunk = self._audio_queue.get()
            if chunk is None:
                return
            yield chunk

    def stream(self) -> Iterator[str]:
        try:
            with self.client.audio.transcriptions.stream(
                model=self.model,
                file=self._audio_source(),
                response_format="text",
            ) as stream:
                for event in stream:
                    event_type = getattr(event, "type", None)
                    if event_type in {"transcription.delta", "transcript.delta"}:
                        delta = getattr(event, "delta", None)
                        if delta:
                            yield delta
                    elif event_type in {"transcription.completed", "transcript.completed"}:
                        text = getattr(event, "text", None)
                        if text:
                            yield text
        finally:
            self._audio_queue.put(None)

    def run_microphone(self, chunk_size: int = 1024, channels: int = 1, format=pyaudio.paInt16) -> Iterator[str]:
        p = pyaudio.PyAudio()
        stream = p.open(
            format=format,
            channels=channels,
            rate=self.sample_rate,
            input=True,
            frames_per_buffer=chunk_size,
        )
        try:
            for _ in self.stream():
                pass
        finally:
            stream.stop_stream()
            stream.close()
            p.terminate()

    def enqueue_audio(self, data: bytes) -> None:
        self._audio_queue.put(data)


def main() -> int:
    streamer = MicrophoneTranscriptStreamer()
    p = pyaudio.PyAudio()
    mic = p.open(
        format=pyaudio.paInt16,
        channels=1,
        rate=16000,
        input=True,
        frames_per_buffer=1024,
    )
    try:
        while True:
            audio = mic.read(1024, exception_on_overflow=False)
            streamer.enqueue_audio(audio)
            for transcript in streamer.stream():
                sys.stdout.write(transcript)
                sys.stdout.flush()
    except KeyboardInterrupt:
        return 0
    finally:
        mic.stop_stream()
        mic.close()
        p.terminate()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
