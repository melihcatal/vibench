from __future__ import annotations

from typing import Any, Iterable, List

from speech_models import TranscriptChunk, normalize_text


class DeepgramPartialResultsHandler:
    def __init__(self) -> None:
        self.interim_buffer: str = ""
        self.finalized: List[TranscriptChunk] = []

    def handle_result(self, result: Any) -> TranscriptChunk | None:
        channel = getattr(result, "channel", None)
        alternatives = getattr(channel, "alternatives", None) if channel is not None else None
        if not alternatives:
            return None

        alt = alternatives[0]
        transcript = normalize_text(getattr(alt, "transcript", ""))
        if not transcript:
            return None

        is_final = bool(getattr(result, "is_final", False) or getattr(result, "speech_final", False))
        confidence = getattr(alt, "confidence", None)
        chunk = TranscriptChunk(
            text=transcript,
            is_final=is_final,
            confidence=confidence,
            raw=result,
        )

        if is_final:
            self.finalized.append(chunk)
            self.interim_buffer = ""
        else:
            self.interim_buffer = transcript
        return chunk

    def finalized_text(self) -> str:
        return " ".join(chunk.text for chunk in self.finalized).strip()

    def current_text(self) -> str:
        base = self.finalized_text()
        return f"{base} {self.interim_buffer}".strip() if self.interim_buffer else base


def extract_transcript_events(results: Iterable[Any]) -> list[TranscriptChunk]:
    handler = DeepgramPartialResultsHandler()
    output: list[TranscriptChunk] = []
    for result in results:
        chunk = handler.handle_result(result)
        if chunk is not None:
            output.append(chunk)
    return output
