# [HELPER] speech_models.py
from typing import NamedTuple, List

# Minimal local models that mirror provider result structures for easier downstream usage.


class Word(NamedTuple):
    start_time: float  # seconds
    end_time: float    # seconds
    word: str


class Alternative(NamedTuple):
    transcript: str
    confidence: float
    words: List[Word] = []


class StreamingRecognitionResult(NamedTuple):
    is_partial: bool
    alternatives: List[Alternative]
    # The provider supplies a confidence score for the whole result when available
    confidence: float = 0.0

    def __str__(self):
        alt = self.alternatives[0] if self.alternatives else Alternative('', 0.0)
        return (f"Partial={self.is_partial} | Transcript='{alt.transcript}' | Confidence={alt.confidence:.2f}")

# Helper normalization function (could be expanded for other providers)

def normalize_provider_result(provider_result):
    """
    Convert a raw provider streaming result into our local StreamingRecognitionResult.
    Currently assumes Google Cloud format; adapt as needed.
    """
    # Example mapping from google.cloud.speech_v1p1beta1.StreamingRecognitionResult
    is_partial = provider_result.is_final is False
    alternatives = [
        Alternative(
            transcript=alt.transcript,
            confidence=alt.confidence,
            words=[Word(start_time=w.start_time.seconds + w.start_time.nanos / 1e9,
                        end_time=e.end_time.seconds + e.end_time.nanos / 1e9,
                        word=w.word)
                   for w in alt.words]
        )
        for alt in provider_result.alternatives
    ]
    # Overall confidence can be taken from the first alternative or a top-level field if present
    confidence = alternatives[0].confidence if alternatives else 0.0
    return StreamingRecognitionResult(is_partial=is_partial,
                                       alternatives=alternatives,
                                       confidence=confidence)
