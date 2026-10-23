from typing import Dict, Any, List
from dataclasses import dataclass


@dataclass
class SpeechRecognitionResult:
    is_final: bool
    transcript: str
    confidence: float
    language_code: str = "en-US"


@dataclass
class NormalizedTranscript:
    text: str
    segments: List[Dict[str, Any]]
    language: str


def normalize_response(result: Dict[str, Any]) -> SpeechRecognitionResult:
    return SpeechRecognitionResult(
        is_final=result["is_final"],
        transcript=result["transcript"],
        confidence=result.get("confidence", 0.0),
    )


def merge_transcripts(
    transcripts: List[SpeechRecognitionResult],
) -> NormalizedTranscript:
    full_text = " ".join([t.transcript for t in transcripts if t.is_final])
    segments = [
        {
            "text": t.transcript,
            "confidence": t.confidence,
            "is_final": t.is_final,
        }
        for t in transcripts
    ]
    return NormalizedTranscript(
        text=full_text, segments=segments, language=transcripts[0].language_code
    )
