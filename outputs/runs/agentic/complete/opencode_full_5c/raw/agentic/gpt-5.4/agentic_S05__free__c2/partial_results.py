from __future__ import annotations

from typing import Any, Iterable

from speech_models import (
    TranscriptEvent,
    merge_finalized_text,
    merge_visible_text,
    normalize_google_streaming_response,
)


class PartialResultAccumulator:
    def __init__(self) -> None:
        self.final_text = ""
        self.partial_text = ""

    def update(self, event: TranscriptEvent) -> dict[str, Any]:
        finalized = merge_finalized_text(event.results)
        visible = merge_visible_text(event.results)
        if finalized:
            self.final_text = " ".join(
                part for part in [self.final_text, finalized] if part
            ).strip()
        self.partial_text = (
            visible if not all(result.is_final for result in event.results) else ""
        )
        return {
            "final_text": self.final_text,
            "partial_text": self.partial_text,
            "provider": "Google Cloud Speech-to-Text",
        }


def handle_streaming_events(responses: Iterable[Any]) -> list[dict[str, Any]]:
    accumulator = PartialResultAccumulator()
    updates: list[dict[str, Any]] = []
    for response in responses:
        event = normalize_google_streaming_response(response)
        if event.results:
            updates.append(accumulator.update(event))
    return updates
