from dataclasses import dataclass
from typing import List, Optional
from google.cloud import speech_v1p1beta1 as speech

@dataclass
class Alternative:
    transcript: str
    confidence: float

@dataclass
class Result:
    alternatives: List[Alternative]
    is_final: bool
    stability: float

@dataclass
class StreamingRecognitionResponse:
    results: List[Result]
    # Add other relevant fields if needed

def normalize_response(response: speech.StreamingRecognizeResponse) -> StreamingRecognitionResponse:
    """Normalizes a Google Cloud Speech-to-Text StreamingRecognizeResponse.

    Args:
        response: The original Google Cloud Speech-to-Text response object.

    Returns:
        A normalized StreamingRecognitionResponse object.
    """
    normalized_results = []
    for result in response.results:
        normalized_alternatives = [
            Alternative(
                transcript=alt.transcript,
                confidence=alt.confidence
            )
            for alt in result.alternatives
        ]
        normalized_results.append(
            Result(
                alternatives=normalized_alternatives,
                is_final=result.is_final,
                stability=result.stability
            )
        )
    return StreamingRecognitionResponse(results=normalized_results)
