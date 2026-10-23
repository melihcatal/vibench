import dataclasses


@dataclasses.dataclass
class StreamingRecognitionRequest:
    audio_content: bytes


@dataclasses.dataclass
class StreamingRecognitionResult:
    transcript: str
    is_final: bool
    confidence: float


def normalize_response(response) -> StreamingRecognitionResult:
    """Normalizes a Google Cloud Speech-to-Text streaming response."""
    if not response.results:
        return StreamingRecognitionResult("", False, 0.0)

    result = response.results[0]
    if not result.alternatives:
        return StreamingRecognitionResult("", False, 0.0)

    alternative = result.alternatives[0]
    return StreamingRecognitionResult(
        transcript=alternative.transcript,
        is_final=result.is_final,
        confidence=alternative.confidence,
    )
