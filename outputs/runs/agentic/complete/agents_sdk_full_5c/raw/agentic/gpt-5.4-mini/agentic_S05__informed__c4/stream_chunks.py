from __future__ import annotations

from collections.abc import AsyncIterable
from typing import AsyncIterator

from speech_client import SpeechClientConfig, StreamingSpeechClient
from speech_models import NormalizedTranscriptEvent, SpeechChunk


async def stream_chunks(chunks: AsyncIterable[SpeechChunk], config: SpeechClientConfig | None = None) -> AsyncIterator[NormalizedTranscriptEvent]:
    client = StreamingSpeechClient(config)
    recognizer = client.start_recognizer()
    recognizer.start()
    async for chunk in chunks:
        recognizer.send(client.chunk_to_audio_payload(chunk))
        for event in getattr(client, "events", []):
            yield event
    recognizer.stop()
