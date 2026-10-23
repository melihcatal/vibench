from __future__ import annotations

from typing import Any, Iterable

from speech_models import (
    TranscriptAccumulator,
    TranscriptChunk,
    collect_normalized_results,
)


class PartialResultsHandler:
    def __init__(self) -> None:
        self.accumulator = TranscriptAccumulator()

    def consume_response(self, response: Any) -> list[TranscriptChunk]:
        chunks = collect_normalized_results(response)
        for chunk in chunks:
            self.accumulator.add(chunk)
        return chunks

    def consume_many(self, responses: Iterable[Any]) -> list[TranscriptChunk]:
        seen: list[TranscriptChunk] = []
        for response in responses:
            seen.extend(self.consume_response(response))
        return seen

    def current_text(self) -> str:
        return self.accumulator.combined_text()

    def final_segments(self) -> list[str]:
        return list(self.accumulator.final_texts)
