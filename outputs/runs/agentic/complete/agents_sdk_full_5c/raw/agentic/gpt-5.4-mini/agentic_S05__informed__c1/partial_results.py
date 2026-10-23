from __future__ import annotations

from typing import List

from speech_models import NormalizedTranscript, RecognitionEvent, TranscriptSegment, normalize_text


class PartialResultHandler:
    def __init__(self) -> None:
        self.partial_text: str = ""
        self.final_segments: List[str] = []

    def handle_event(self, event: RecognitionEvent) -> NormalizedTranscript:
        if not event.segments:
            return NormalizedTranscript(text="", final=False, raw={"event": event.raw})
        latest = event.segments[-1]
        text = normalize_text(latest.text)
        if latest.is_final:
            self.final_segments.append(text)
            self.partial_text = ""
        else:
            self.partial_text = text
        return NormalizedTranscript(
            text=self.combined_text(),
            final=latest.is_final,
            language_code=latest.language_code,
            confidence=latest.stability,
            raw=event.raw,
        )

    def combined_text(self) -> str:
        pieces = [segment for segment in self.final_segments if segment]
        if self.partial_text:
            pieces.append(self.partial_text)
        return " ".join(pieces)
