from __future__ import annotations

from typing import Any, AsyncIterator, Iterable, Iterator, List

from speech_models import TranscriptChunk, normalize_google_result


async def iter_transcript_events(responses: Any) -> AsyncIterator[TranscriptChunk]:
    async for response in responses:
        for result in getattr(response, "results", []):
            chunk = normalize_google_result(result)
            if chunk.text:
                yield chunk


def split_partial_and_final(
    chunks: Iterable[TranscriptChunk],
) -> tuple[list[TranscriptChunk], list[TranscriptChunk]]:
    partial: List[TranscriptChunk] = []
    final: List[TranscriptChunk] = []
    for chunk in chunks:
        if chunk.is_final:
            final.append(chunk)
        else:
            partial.append(chunk)
    return partial, final
