from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class ResultType(Enum):
    INTERIM = "interim"
    FINAL = "final"


@dataclass
class WordInfo:
    word: str
    start_offset_ms: int = 0
    end_offset_ms: int = 0
    confidence: float = 0.0


@dataclass
class Alternative:
    transcript: str
    confidence: float = 0.0
    words: List[WordInfo] = field(default_factory=list)


@dataclass
class RecognitionResult:
    result_id: str
    alternatives: List[Alternative]
    result_type: ResultType
    language_code: str = "en-US"
    is_final: bool = False
    stability: float = 0.0
    audio_processed_ms: int = 0

    @property
    def best_transcript(self) -> str:
        if self.alternatives:
            return self.alternatives[0].transcript
        return ""

    @property
    def best_confidence(self) -> float:
        if self.alternatives:
            return self.alternatives[0].confidence
        return 0.0


@dataclass
class StreamingRequest:
    audio_content: bytes
    is_end: bool = False


@dataclass
class StreamConfig:
    project_id: str
    model: str = "latest_long"
    language_code: str = "en-US"
    location: str = "global"
    sample_rate_hertz: int = 16000
    encoding: str = "LINEAR16"
    audio_channel_count: int = 1
    enable_automatic_punctuation: bool = True
    enable_word_time_offsets: bool = True
    profanity_filter: bool = False
    max_alternatives: int = 1
    interim_results: bool = True


def normalize_google_response(response) -> RecognitionResult:
    from google.cloud.speech_v2.types import cloud_speech

    result = response.results[0]
    alternatives = []
    for alt in result.alternatives:
        words = [
            WordInfo(
                word=w.word,
                start_offset_ms=int(w.start_offset.total_seconds() * 1000)
                if w.start_offset
                else 0,
                end_offset_ms=int(w.end_offset.total_seconds() * 1000)
                if w.end_offset
                else 0,
                confidence=w.confidence,
            )
            for w in alt.words
        ]
        alternatives.append(
            Alternative(
                transcript=alt.transcript,
                confidence=alt.confidence,
                words=words,
            )
        )

    is_final = result.is_final
    return RecognitionResult(
        result_id=str(result.result_id),
        alternatives=alternatives,
        result_type=ResultType.FINAL if is_final else ResultType.INTERIM,
        language_code=result.language_code,
        is_final=is_final,
        stability=result.stability,
        audio_processed_ms=int(result.audio_processed_duration.total_seconds() * 1000)
        if result.audio_processed_duration
        else 0,
    )


def build_streaming_request(audio_bytes: bytes, is_end: bool = False) -> dict:
    from google.cloud.speech_v2.types import cloud_speech

    if is_end:
        return cloud_speech.StreamingRecognizeRequest(
            streaming_features=cloud_speech.StreamingRecognitionFeatures(
                interim_results=True,
            ),
        )

    return cloud_speech.StreamingRecognizeRequest(
        audio=audio_bytes,
    )


def chunk_audio_buffer(buffer: bytes, chunk_size: int = 6400) -> List[bytes]:
    chunks = []
    for i in range(0, len(buffer), chunk_size):
        chunks.append(buffer[i : i + chunk_size])
    return chunks


def merge_transcripts(results: List[RecognitionResult]) -> str:
    final_parts = []
    interim_parts = []
    for r in results:
        if r.is_final:
            final_parts.append(r.best_transcript)
        else:
            interim_parts.append(r.best_transcript)
    if final_parts:
        return " ".join(final_parts)
    if interim_parts:
        return " ".join(interim_parts)
    return ""
