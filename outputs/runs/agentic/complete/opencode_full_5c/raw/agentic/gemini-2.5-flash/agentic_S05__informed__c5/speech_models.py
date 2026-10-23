import dataclasses
from typing import List, Optional


@dataclasses.dataclass
class SpeechRecognitionRequest:
    audio_content: bytes
    sample_rate_hertz: int = 16000
    language_code: str = "en-US"
    enable_automatic_punctuation: bool = True
    interim_results: bool = True


@dataclasses.dataclass
class SpeechRecognitionAlternative:
    transcript: str
    confidence: float


@dataclasses.dataclass
class SpeechRecognitionResult:
    alternatives: List[SpeechRecognitionAlternative]
    is_final: bool


@dataclasses.dataclass
class SpeechRecognitionResponse:
    results: List[SpeechRecognitionResult]


def normalize_google_speech_response(google_response):
    results = []
    for gr in google_response.results:
        alternatives = [
            SpeechRecognitionAlternative(
                transcript=alt.transcript, confidence=alt.confidence
            )
            for alt in gr.alternatives
        ]
        results.append(
            SpeechRecognitionResult(alternatives=alternatives, is_final=gr.is_final)
        )
    return SpeechRecognitionResponse(results=results)
