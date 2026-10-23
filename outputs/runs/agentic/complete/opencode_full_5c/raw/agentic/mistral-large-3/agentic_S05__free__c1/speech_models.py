from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SpeechRecognitionResult:
    """Represents a speech recognition result."""

    transcript: str
    is_final: bool
    stability: float = 0.0


@dataclass
class StreamingRecognitionResponse:
    """Represents a streaming recognition response."""

    results: List[SpeechRecognitionResult]


def normalize_response(response: Dict[str, Any]) -> StreamingRecognitionResponse:
    """Normalizes a raw streaming recognition response."""
    results = []
    for result in response.get("results", []):
        alternatives = result.get("alternatives", [{}])[0]
        results.append(
            SpeechRecognitionResult(
                transcript=alternatives.get("transcript", ""),
                is_final=result.get("is_final", False),
                stability=result.get("stability", 0.0),
            )
        )
    return StreamingRecognitionResponse(results=results)
