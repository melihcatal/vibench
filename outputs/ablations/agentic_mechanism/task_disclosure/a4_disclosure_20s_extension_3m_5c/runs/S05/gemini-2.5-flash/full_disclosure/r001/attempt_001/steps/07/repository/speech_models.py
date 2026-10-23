import dataclasses
from typing import List, Dict, Any

@dataclasses.dataclass
class RecognitionConfig:
    encoding: str = "LINEAR16"
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    model: str = "default"
    max_alternatives: int = 1

@dataclasses.dataclass
class StreamingRecognitionConfig:
    config: RecognitionConfig
    interim_results: bool = True

@dataclasses.dataclass
class StreamingSpeechRecognitionRequest:
    audio_content: bytes = dataclasses.field(default=b"", repr=False)
    streaming_config: StreamingRecognitionConfig = dataclasses.field(default_factory=lambda: StreamingRecognitionConfig(config=RecognitionConfig()))

@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float = 0.0

@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool

@dataclasses.dataclass
class StreamingSpeechRecognitionResponse:
    results: List[SpeechRecognitionResult]

def _normalize_response(response: Dict[str, Any]) -> StreamingSpeechRecognitionResponse:
    """Normalizes a raw API response into a StreamingSpeechRecognitionResponse object."""
    results = []
    for res_data in response.get("results", []):
        alternatives = []
        for alt_data in res_data.get("alternatives", []):
            alternatives.append(SpeechRecognitionAlternative(
                transcript=alt_data.get("transcript", ""),
                confidence=alt_data.get("confidence", 0.0)
            ))
        results.append(SpeechRecognitionResult(
            alternatives=alternatives,
            is_final=res_data.get("is_final", False)
        ))
    return StreamingSpeechRecognitionResponse(results=results)
