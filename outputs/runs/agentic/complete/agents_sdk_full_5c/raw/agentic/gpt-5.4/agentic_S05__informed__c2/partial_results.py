from __future__ import annotations

import asyncio
from typing import AsyncIterable, Iterable, Iterator, List

from speech_models import TranscriptSegment, normalize_transcript_text



def _result_to_segment(result) -> TranscriptSegment:
    if not result.alternatives:
        return TranscriptSegment(text="", is_final=getattr(result, "is_final", False))
    alt = result.alternatives[0]
    return TranscriptSegment(
        text=normalize_transcript_text(getattr(alt, "transcript", "")),
        is_final=getattr(result, "is_final", False),
        confidence=getattr(alt, "confidence", None),
        language=None,
        words=[{"word": getattr(word, "word", "")} for word in getattr(alt, "words", [])],
    )



def iter_transcript_events(responses: Iterable) -> Iterator[TranscriptSegment]:
    for response in responses:
        for result in getattr(response, "results", []):
            segment = _result_to_segment(result)
            if segment.text:
                yield segment


async def collect_transcript_events(responses: Iterable | AsyncIterable) -> List[TranscriptSegment]:
    items: List[TranscriptSegment] = []
    if hasattr(responses, "__aiter__"):
        async for response in responses:
            for result in getattr(response, "results", []):
                segment = _result_to_segment(result)
                if segment.text:
                    items.append(segment)
            await asyncio.sleep(0)
        return items

    for response in responses:
        for result in getattr(response, "results", []):
            segment = _result_to_segment(result)
            if segment.text:
                items.append(segment)
        await asyncio.sleep(0)
    return items
