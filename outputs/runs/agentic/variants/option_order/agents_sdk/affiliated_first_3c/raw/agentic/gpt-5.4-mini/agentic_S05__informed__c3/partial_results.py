from __future__ import annotations

from typing import Iterable, List

from speech_models import TranscriptChunk, normalize_chunks


class PartialResultHandler:
    def __init__(self) -> None:
        self._partials: List[TranscriptChunk] = []
        self._finals: List[TranscriptChunk] = []

    def handle_event(self, text: str, is_final: bool, speaker: str | None = None) -> TranscriptChunk:
        chunk = TranscriptChunk(text=text, is_final=is_final, speaker=speaker, metadata={"provider": "azure-speech"})
        if is_final:
            self._finals.append(chunk)
        else:
            self._partials.append(chunk)
        return chunk

    def merged(self) -> List[TranscriptChunk]:
        return normalize_chunks([*self._partials, *self._finals])


def handle_partial_and_final_events(events: Iterable[tuple[str, bool]]) -> List[TranscriptChunk]:
    handler = PartialResultHandler()
    for text, is_final in events:
        handler.handle_event(text=text, is_final=is_final)
    return handler.merged()
