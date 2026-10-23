from dataclasses import dataclass
from typing import List


@dataclass
class StreamingTranscript:
    transcript: str
    is_final: bool
    stability: float


def normalize_response(response: object) -> List[StreamingTranscript]:
    """Normalizes a streaming speech recognition response."""
    normalized_results = []
    if not response.results:
        return normalized_results

    result = response.results[0]
    if not result.alternatives:
        return normalized_results

    normalized_results.append(
        StreamingTranscript(
            transcript=result.alternatives[0].transcript,
            is_final=result.is_final,
            stability=result.stability,
        )
    )
    return normalized_results
