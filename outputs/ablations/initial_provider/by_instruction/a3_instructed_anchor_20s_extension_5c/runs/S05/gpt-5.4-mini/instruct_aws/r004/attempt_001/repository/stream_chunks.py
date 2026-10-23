from typing import AsyncIterable, Iterable, Iterator

from speech_client import stream_transcribe
from speech_models import StreamingAudioChunk


def stream_audio_chunks(source: AsyncIterable[bytes], sample_rate_hz: int) -> Iterator[str]:
    async def _collect() -> Iterable[StreamingAudioChunk]:
        chunks = []
        async for payload in source:
            chunks.append(StreamingAudioChunk(payload=payload, sample_rate_hz=sample_rate_hz))
        return chunks

    import asyncio

    chunks = asyncio.run(_collect())
    for segment in stream_transcribe(chunks):
        if segment.text:
            yield segment.text
