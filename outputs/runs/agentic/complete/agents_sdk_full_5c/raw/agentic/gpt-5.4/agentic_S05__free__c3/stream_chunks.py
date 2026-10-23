from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator
from queue import Queue
from typing import Optional

import azure.cognitiveservices.speech as speechsdk

from partial_results import PartialResultHandler
from speech_client import create_push_stream, create_speech_recognizer
from speech_models import StreamingRecognitionConfig, TranscriptEvent


class AsyncChunkSpeechStreamer:
    def __init__(self, config: Optional[StreamingRecognitionConfig] = None) -> None:
        self.config = config or StreamingRecognitionConfig()
        self.push_stream, self.audio_config = create_push_stream(
            sample_rate_hz=self.config.sample_rate_hz,
            channels=self.config.channels,
        )
        self.recognizer = create_speech_recognizer(self.config, audio_config=self.audio_config)
        self._queue: Queue[TranscriptEvent] = Queue()
        self._handler = PartialResultHandler(on_event=self._queue.put)
        self._handler.bind(self.recognizer)
        self._done = False
        self.recognizer.session_stopped.connect(lambda evt: setattr(self, "_done", True))
        self.recognizer.canceled.connect(lambda evt: setattr(self, "_done", True))

    async def stream(self, audio_source: AsyncIterator[bytes]) -> AsyncIterator[TranscriptEvent]:
        self.recognizer.start_continuous_recognition()
        producer = asyncio.create_task(self._feed_audio(audio_source))
        try:
            while not self._done or not self._queue.empty() or not producer.done():
                try:
                    event = self._queue.get_nowait()
                    if self.config.interim_results or event.is_final:
                        yield event
                except Exception:
                    await asyncio.sleep(0.05)
            await producer
        finally:
            self.recognizer.stop_continuous_recognition()

    async def _feed_audio(self, audio_source: AsyncIterator[bytes]) -> None:
        async for chunk in audio_source:
            if chunk:
                self.push_stream.write(chunk)
        self.push_stream.close()
