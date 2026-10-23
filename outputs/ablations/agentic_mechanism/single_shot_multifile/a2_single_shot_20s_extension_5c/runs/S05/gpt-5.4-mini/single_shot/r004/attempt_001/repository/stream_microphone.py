import asyncio
import os
from typing import AsyncIterator, Iterator, Optional

import pyaudio
from deepgram import DeepgramClient, LiveTranscriptionEvents, LiveOptions

from speech_client import build_deepgram_client, load_speech_config
from speech_models import TranscriptEvent, normalize_transcript_event


class MicrophoneStream:
    def __init__(self, rate: int = 16000, chunk_size: int = 1024) -> None:
        self.rate = rate
        self.chunk_size = chunk_size
        self._audio = pyaudio.PyAudio()
        self._stream = None

    def __enter__(self):
        self._stream = self._audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.rate,
            input=True,
            frames_per_buffer=self.chunk_size,
        )
        return self

    def __exit__(self, exc_type, exc, tb):
        if self._stream is not None:
            self._stream.stop_stream()
            self._stream.close()
        self._audio.terminate()

    def generator(self) -> Iterator[bytes]:
        while True:
            data = self._stream.read(self.chunk_size, exception_on_overflow=False)
            if not data:
                continue
            yield data


async def stream_microphone() -> AsyncIterator[TranscriptEvent]:
    config = load_speech_config()
    client = build_deepgram_client()
    stream = client.listen.websocket.v("1")
    options = LiveOptions(
        model=config.model,
        language=config.language,
        punctuate=config.punctuate,
        interim_results=True,
        endpointing=config.endpointing,
        smart_format=True,
    )
    queue: asyncio.Queue[TranscriptEvent] = asyncio.Queue()

    def on_message(_self, result, **kwargs):
        event = normalize_transcript_event(result)
        if event is not None:
            queue.put_nowait(event)

    stream.on(LiveTranscriptionEvents.Transcript, on_message)
    with MicrophoneStream(rate=config.sample_rate, chunk_size=config.chunk_size) as mic:
        await stream.start(options)
        try:
            for chunk in mic.generator():
                await stream.send(chunk)
                while not queue.empty():
                    yield await queue.get()
        finally:
            await stream.finish()


async def main() -> None:
    async for event in stream_microphone():
        if event.text:
            print(event.text)


if __name__ == "__main__":
    asyncio.run(main())
