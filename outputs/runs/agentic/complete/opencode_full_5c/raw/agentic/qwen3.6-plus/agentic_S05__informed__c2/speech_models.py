import time
import uuid
from dataclasses import dataclass, field
from typing import List, Optional
from enum import Enum


class TranscriptType(str, Enum):
    INTERIM = "interim"
    FINAL = "final"


@dataclass
class AudioChunk:
    data: bytes
    sample_rate: int = 16000
    channels: int = 1
    timestamp: float = field(default_factory=time.time)
    chunk_id: str = field(default_factory=lambda: str(uuid.uuid4()))

    @property
    def duration_seconds(self) -> float:
        bytes_per_sample = 2
        return len(self.data) / (self.sample_rate * self.channels * bytes_per_sample)


@dataclass
class WordInfo:
    word: str
    start: float = 0.0
    end: float = 0.0
    confidence: float = 0.0
    speaker: Optional[str] = None


@dataclass
class TranscriptResult:
    text: str
    transcript_type: TranscriptType = TranscriptType.INTERIM
    confidence: float = 0.0
    words: List[WordInfo] = field(default_factory=list)
    language: str = "en-US"
    channel: int = 0
    timestamp: float = field(default_factory=time.time)
    result_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    is_final: bool = False
    speech_final: bool = False
    duration: float = 0.0
    start_time: float = 0.0

    @property
    def is_interim(self) -> bool:
        return self.transcript_type == TranscriptType.INTERIM


@dataclass
class StreamingSession:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    model: str = "nova-2"
    language: str = "en-US"
    sample_rate: int = 16000
    channels: int = 1
    started_at: float = field(default_factory=time.time)
    results: List[TranscriptResult] = field(default_factory=list)
    is_active: bool = False

    def add_result(self, result: TranscriptResult):
        self.results.append(result)

    def get_final_transcript(self) -> str:
        final_texts = [r.text for r in self.results if r.is_final]
        return " ".join(final_texts)

    def get_all_transcript(self) -> str:
        return " ".join(r.text for r in self.results if r.text.strip())


def parse_deepgram_result(raw_result: dict) -> TranscriptResult:
    channel = raw_result.get("channel_index", [0])[0]
    alternatives = raw_result.get("alternatives", [])
    if not alternatives:
        return TranscriptResult(
            text="",
            transcript_type=TranscriptType.INTERIM,
            is_final=False,
            channel=channel,
        )

    alt = alternatives[0]
    text = alt.get("transcript", "").strip()
    confidence = alt.get("confidence", 0.0)
    is_final = raw_result.get("is_final", False)
    speech_final = raw_result.get("speech_final", False)
    start_time = raw_result.get("start", 0.0)
    duration = raw_result.get("duration", 0.0)

    words = []
    for w in alt.get("words", []):
        words.append(
            WordInfo(
                word=w.get("word", ""),
                start=w.get("start", 0.0),
                end=w.get("end", 0.0),
                confidence=w.get("confidence", 0.0),
                speaker=w.get("speaker"),
            )
        )

    return TranscriptResult(
        text=text,
        transcript_type=TranscriptType.FINAL if is_final else TranscriptType.INTERIM,
        confidence=confidence,
        words=words,
        is_final=is_final,
        speech_final=speech_final,
        duration=duration,
        start_time=start_time,
        channel=channel,
    )


def normalize_transcript_text(text: str) -> str:
    text = text.strip()
    text = " ".join(text.split())
    return text


def merge_consecutive_results(
    results: List[TranscriptResult],
) -> List[TranscriptResult]:
    if not results:
        return []

    merged = []
    current_text_parts = []
    current_confidences = []
    current_words = []
    start_time = results[0].start_time

    for result in results:
        if result.is_final and current_text_parts:
            merged_text = normalize_transcript_text(" ".join(current_text_parts))
            avg_confidence = (
                sum(current_confidences) / len(current_confidences)
                if current_confidences
                else 0.0
            )
            merged.append(
                TranscriptResult(
                    text=merged_text,
                    transcript_type=TranscriptType.FINAL,
                    confidence=avg_confidence,
                    words=current_words,
                    is_final=True,
                    speech_final=True,
                    start_time=start_time,
                    duration=result.start_time + result.duration - start_time,
                )
            )
            current_text_parts = []
            current_confidences = []
            current_words = []
            start_time = result.start_time + result.duration

        if result.text:
            current_text_parts.append(result.text)
            if result.confidence > 0:
                current_confidences.append(result.confidence)
            current_words.extend(result.words)

    if current_text_parts:
        merged_text = normalize_transcript_text(" ".join(current_text_parts))
        avg_confidence = (
            sum(current_confidences) / len(current_confidences)
            if current_confidences
            else 0.0
        )
        last = results[-1]
        merged.append(
            TranscriptResult(
                text=merged_text,
                transcript_type=TranscriptType.INTERIM,
                confidence=avg_confidence,
                words=current_words,
                is_final=False,
                speech_final=False,
                start_time=start_time,
                duration=last.start_time + last.duration - start_time
                if results
                else 0.0,
            )
        )

    return merged
