from dataclasses import dataclass


@dataclass
class TranscriptResult:
    transcript: str
    is_final: bool
    confidence: float = 0.0


def normalize_transcript_response(response) -> TranscriptResult:
    """Normalizes a Google Cloud Speech-to-Text streaming response."""
    if not response.results:
        return TranscriptResult(transcript="", is_final=False)

    result = response.results[0]
    if not result.alternatives:
        return TranscriptResult(transcript="", is_final=result.is_final)

    alternative = result.alternatives[0]
    return TranscriptResult(
        transcript=alternative.transcript,
        is_final=result.is_final,
        confidence=alternative.confidence,
    )
