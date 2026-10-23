from typing import AsyncIterator, Dict, Any

from speech_models import TranscriptChunk, normalize_transcript


async def partial_results(
    events: AsyncIterator[Dict[str, Any]],
) -> AsyncIterator[TranscriptChunk]:
    async for event in events:
        chunk = normalize_transcript(event)
        if chunk.text:
            yield TranscriptChunk(
                text=chunk.text,
                is_final=chunk.is_final,
                language=chunk.language,
                alternatives=chunk.alternatives,
            )
