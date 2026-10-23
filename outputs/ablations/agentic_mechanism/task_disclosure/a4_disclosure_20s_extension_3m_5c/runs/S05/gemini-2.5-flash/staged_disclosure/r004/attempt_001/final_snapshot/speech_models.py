import dataclasses
from typing import List

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = False

@dataclasses.dataclass
class StreamingRecognitionRequest:
    audio_content: bytes = b""
    config: RecognitionConfig = dataclasses.field(default_factory=RecognitionConfig)

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str = ""
    confidence: float = 0.0

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative] = dataclasses.field(default_factory=list)
    is_final: bool = False

@dataclasses.dataclass
class StreamingRecognitionResponse:
    results: List[SpeechRecognitionResult] = dataclasses.field(default_factory=list)

def normalize_response(response: StreamingRecognitionResponse) -> dict:
    normalized_results = []
    for result in response.results:
        normalized_alternatives = []
        for alternative in result.alternatives:
            normalized_alternatives.append({
                "transcript": alternative.transcript,
                "confidence": alternative.confidence
            })
        normalized_results.append({
            "alternatives": normalized_alternatives,
            "is_final": result.is_final
        })
    return {"results": normalized_results}
