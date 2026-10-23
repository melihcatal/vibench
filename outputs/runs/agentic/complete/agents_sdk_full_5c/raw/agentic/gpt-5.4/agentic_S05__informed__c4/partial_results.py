from __future__ import annotations

from typing import Any, Optional

from speech_models import TranscriptAccumulator, TranscriptSegment, normalize_transcript_text


class PartialResultHandler:
    def __init__(self) -> None:
        self.accumulator = TranscriptAccumulator()

    def from_deepgram_result(self, result: Any) -> Optional[TranscriptSegment]:
        alternative = result.channel.alternatives[0]
        text = normalize_transcript_text(alternative.transcript)
        if not text:
            return None
        return TranscriptSegment(
            text=text,
            is_final=bool(getattr(result, "is_final", False)),
            confidence=getattr(alternative, "confidence", None),
            raw=result,
        )

    def consume(self, result: Any) -> Optional[dict[str, Any]]:
        segment = self.from_deepgram_result(result)
        if segment is None:
            return None
        composed = self.accumulator.apply(segment)
        return {
            "text": segment.text,
            "is_final": segment.is_final,
            "confidence": segment.confidence,
            "composed_text": composed,
            "final_text": " ".join(self.accumulator.final_texts).strip(),
            "provider": "deepgram",
        }
