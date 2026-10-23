from typing import AsyncIterator, Iterable
from speech_client import build_client
from speech_models import TranscriptChunk, normalize_transcript_payload

async def stream_chunks(chunks: AsyncIterator[bytes]) -> AsyncIterator[TranscriptChunk]:
    client = build_client()
    collected = bytearray()
    async for chunk in chunks:
        collected.extend(chunk)
    response = client.audio.transcriptions.create(
        model="gpt-4o-mini-transcribe",
        file=("chunks.wav", bytes(collected)),
        response_format="verbose_json",
    )
    yield normalize_transcript_payload({"text": getattr(response, "text", ""), "final": True})
