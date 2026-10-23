from dataclasses import dataclass
from typing import Optional, List


@dataclass
class PartialResult:
    """Represents a partial streaming recognition result."""

    transcript: str
    confidence: Optional[float] = None
    stability: Optional[float] = None
    words: Optional[List[dict]] = None

    @classmethod
    def from_grpc(cls, result):
        alternatives = result.alternatives[0]
        return cls(
            transcript=alternatives.transcript,
            confidence=alternatives.confidence,
            stability=getattr(result, "stability", None),
            words=[
                {
                    "word": word.word,
                    "start_time": word.start_time.total_seconds(),
                    "end_time": word.end_time.total_seconds(),
                }
                for word in alternatives.words
            ]
            if hasattr(alternatives, "words")
            else None,
        )


@dataclass
class FinalResult:
    """Represents a final streaming recognition result."""

    transcript: str
    confidence: Optional[float] = None
    words: Optional[List[dict]] = None

    @classmethod
    def from_grpc(cls, result):
        alternatives = result.alternatives[0]
        return cls(
            transcript=alternatives.transcript,
            confidence=alternatives.confidence,
            words=[
                {
                    "word": word.word,
                    "start_time": word.start_time.total_seconds(),
                    "end_time": word.end_time.total_seconds(),
                }
                for word in alternatives.words
            ]
            if hasattr(alternatives, "words")
            else None,
        )


def handle_partial_result(result: PartialResult):
    """Handles a partial recognition result."""
    print(f"Partial: {result.transcript} (Stability: {result.stability})")


def handle_final_result(result: FinalResult):
    """Handles a final recognition result."""
    print(f"Final: {result.transcript} (Confidence: {result.confidence})")
