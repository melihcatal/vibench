import asyncio
from typing import AsyncGenerator, AsyncIterable, Union

from speech_client import SpeechClient
from speech_models import SpeechEvent, SpeechNormalizer


class AudioChunkStreamer:
    """Streams audio chunks from an async source and yields interim transcripts using DashScope."""

    def __init__(self):
        self.client = SpeechClient()
        self.normalizer = SpeechNormalizer()
        self.recognition = self.client.get_recognition_config()

    async def stream_chunks(
        self, audio_source: AsyncIterable[bytes]
    ) -> AsyncGenerator[SpeechEvent, None]:
        """Stream audio chunks and yield interim transcripts."""
        queue = asyncio.Queue()

        async def process_chunks():
            async for chunk in audio_source:
                result = self.recognition.call(chunk)
                if result:
                    event = self.normalizer.normalize_result(result)
                    await queue.put(event)
            await queue.put(None)  # Sentinel to indicate completion

        asyncio.create_task(process_chunks())

        while True:
            event = await queue.get()
            if event is None:
                break
            yield event
