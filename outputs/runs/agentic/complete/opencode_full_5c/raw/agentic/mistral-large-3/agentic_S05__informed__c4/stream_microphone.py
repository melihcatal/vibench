import os
import asyncio
import logging
import pyaudio
from typing import AsyncGenerator

from speech_client import SpeechClient
from speech_models import SpeechEvent, SpeechNormalizer


class MicrophoneStreamer:
    """Streams microphone audio and yields interim transcripts using DashScope."""

    def __init__(self):
        self.client = SpeechClient()
        self.normalizer = SpeechNormalizer()
        self.logger = logging.getLogger(__name__)
        self.audio = pyaudio.PyAudio()
        self.stream = None
        self.recognition = self.client.get_recognition_config()

    async def stream_microphone(self) -> AsyncGenerator[SpeechEvent, None]:
        """Stream microphone audio and yield interim transcripts."""

        def audio_callback(in_data, frame_count, time_info, status):
            """Callback to feed audio chunks to DashScope."""
            try:
                result = self.recognition.call(in_data)
                if result:
                    event = self.normalizer.normalize_result(result)
                    asyncio.run_coroutine_threadsafe(
                        self._yield_event(event), asyncio.get_event_loop()
                    )
            except Exception as e:
                self.logger.error(f"Audio callback error: {e}")
            return (None, pyaudio.paContinue)

    async def _yield_event(self, event: SpeechEvent):
        """Yield a speech event to the async generator."""
        if hasattr(self, "_queue"):
            await self._queue.put(event)

    async def __aenter__(self):
        """Initialize microphone stream and DashScope recognition."""
        self._queue = asyncio.Queue()
        self.stream = self.audio.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=16000,
            input=True,
            frames_per_buffer=1024,
            stream_callback=self.audio_callback,
        )
        self.stream.start_stream()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Cleanup microphone stream and DashScope recognition."""
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.audio.terminate()
        if self.recognition:
            self.recognition.close()

    async def __aiter__(self) -> AsyncGenerator[SpeechEvent, None]:
        """Async iterator to yield speech events."""
        while True:
            event = await self._queue.get()
            if event.is_final:
                self._queue.task_done()
                break
            yield event
            self._queue.task_done()
        while not self._queue.empty():
            event = await self._queue.get()
            yield event
            self._queue.task_done()
