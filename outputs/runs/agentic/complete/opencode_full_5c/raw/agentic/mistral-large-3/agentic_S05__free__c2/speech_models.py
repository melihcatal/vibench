from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SpeechRecognitionResult:
    transcript: str
    is_final: bool
    stability: float
    confidence: float = 0.0


@dataclass
class StreamingRecognitionResponse:
    results: List[SpeechRecognitionResult]
    error: Optional[Dict[str, Any]] = None


def normalize_response(response: Dict[str, Any]) -> StreamingRecognitionResponse:
    results = []
    for result in response.get("results", []):
        alternatives = result.get("alternatives", [])
        if alternatives:
            transcript = alternatives[0].get("transcript", "")
            confidence = alternatives[0].get("confidence", 0.0)
            results.append(
                SpeechRecognitionResult(
                    transcript=transcript,
                    is_final=result.get("is_final", False),
                    stability=result.get("stability", 0.0),
                    confidence=confidence,
                )
            )
    return StreamingRecognitionResponse(results=results)


def merge_transcripts(results: List[SpeechRecognitionResult]) -> str:
    return " ".join([result.transcript for result in results if result.is_final])
