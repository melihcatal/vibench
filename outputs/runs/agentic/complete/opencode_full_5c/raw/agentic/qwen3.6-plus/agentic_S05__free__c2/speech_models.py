import re
from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Optional


@dataclass
class WordInfo:
    word: str
    start_offset_seconds: float
    end_offset_seconds: float
    confidence: float


@dataclass
class StreamingRecognitionResult:
    transcript: str
    is_final: bool
    stability: float
    confidence: float
    words: List[WordInfo] = field(default_factory=list)
    language_code: str = "en-US"
    result_end_time: Optional[float] = None


@dataclass
class StreamingRecognitionRequest:
    audio_chunk: bytes
    chunk_index: int
    timestamp: datetime = field(default_factory=datetime.utcnow)
    is_end_of_stream: bool = False


@dataclass
class StreamingRecognitionResponse:
    results: List[StreamingRecognitionResult]
    total_audio_seconds: float
    request_id: str = ""


def normalize_transcript(text: str) -> str:
    text = text.strip()
    text = re.sub(r"\s+", " ", text)
    if text and not text.endswith((".", "!", "?", ",", ";", ":")):
        text = text[0].upper() + text[1:]
    return text


def merge_results(results: List[StreamingRecognitionResult]) -> str:
    final_parts = []
    interim_parts = []
    for result in results:
        if result.is_final:
            final_parts.append(result.transcript)
        else:
            interim_parts.append(result.transcript)
    combined = " ".join(final_parts + interim_parts)
    return normalize_transcript(combined)


def result_to_dict(result: StreamingRecognitionResult) -> dict:
    return {
        "transcript": result.transcript,
        "is_final": result.is_final,
        "stability": result.stability,
        "confidence": result.confidence,
        "words": [
            {
                "word": w.word,
                "start": w.start_offset_seconds,
                "end": w.end_offset_seconds,
                "confidence": w.confidence,
            }
            for w in result.words
        ],
        "language_code": result.language_code,
    }


def dict_to_result(data: dict) -> StreamingRecognitionResult:
    words = [
        WordInfo(
            word=w["word"],
            start_offset_seconds=w["start"],
            end_offset_seconds=w["end"],
            confidence=w["confidence"],
        )
        for w in data.get("words", [])
    ]
    return StreamingRecognitionResult(
        transcript=data["transcript"],
        is_final=data["is_final"],
        stability=data.get("stability", 0.0),
        confidence=data.get("confidence", 0.0),
        words=words,
        language_code=data.get("language_code", "en-US"),
    )
