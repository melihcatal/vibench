from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class RecognitionAlternative:
    transcript: str
    confidence: float = 0.0


@dataclass
class RecognitionResult:
    alternatives: List[RecognitionAlternative] = field(default_factory=list)
    is_final: bool = False
    stability: float = 0.0


@dataclass
class StreamingRecognitionResponse:
    results: List[RecognitionResult] = field(default_factory=list)
    end_of_utterance: bool = False


@dataclass
class StreamingRecognitionRequest:
    audio_content: Optional[bytes] = None
    sample_rate_hertz: Optional[int] = None
    language_code: Optional[str] = None
    enable_automatic_punctuation: Optional[bool] = None


def normalize_response(speech_response) -> StreamingRecognitionResponse:
    """Normalizes a Google Cloud Speech-to-Text response to a local StreamingRecognitionResponse."""
    normalized_results = []
    for result in speech_response.results:
        normalized_alternatives = []
        for alt in result.alternatives:
            normalized_alternatives.append(
                RecognitionAlternative(
                    transcript=alt.transcript, confidence=alt.confidence
                )
            )
        normalized_results.append(
            RecognitionResult(
                alternatives=normalized_alternatives,
                is_final=result.is_final,
                stability=result.stability,
            )
        )
    return StreamingRecognitionResponse(results=normalized_results)
