from __future__ import annotations

from typing import Iterable, List

from speech_client import transcript_chunk_from_event
from speech_models import StreamResult, TranscriptChunk


def handle_partial_and_final_events(events: Iterable[object]) -> StreamResult:
    result = StreamResult()
    for event in events:
        chunk = transcript_chunk_from_event(event)
        if not chunk.text:
            continue
        result.add(chunk)
    return result


def split_partial_final(chunks: Iterable[TranscriptChunk]) -> tuple[List[str], List[str]]:
    partials: List[str] = []
    finals: List[str] = []
    for chunk in chunks:
        if chunk.is_final:
            finals.append(chunk.text)
        else:
            partials.append(chunk.text)
    return partials, finals
