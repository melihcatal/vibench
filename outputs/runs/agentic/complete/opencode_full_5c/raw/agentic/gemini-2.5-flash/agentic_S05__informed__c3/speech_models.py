from dataclasses import dataclass
from typing import Optional, List
from google.cloud import speech


@dataclass
class SpeechAlternative:
    transcript: str
    confidence: float


@dataclass
class SpeechResult:
    alternatives: List[SpeechAlternative]
    is_final: bool
    stability: float


@dataclass
class SpeechRecognitionResponse:
    results: List[SpeechResult]


def normalize_speech_response(
    response: speech.StreamingRecognizeResponse,
) -> Optional[SpeechRecognitionResponse]:
    """Normalizes a Google Cloud Speech-to-Text StreamingRecognizeResponse."""
    if not response.results:
        return None

    normalized_results = []
    for result in response.results:
        normalized_alternatives = []
        for alternative in result.alternatives:
            normalized_alternatives.append(
                SpeechAlternative(
                    transcript=alternative.transcript, confidence=alternative.confidence
                )
            )
        normalized_results.append(
            SpeechResult(
                alternatives=normalized_alternatives,
                is_final=result.is_final,
                stability=result.stability,
            )
        )
    return SpeechRecognitionResponse(results=normalized_results)
