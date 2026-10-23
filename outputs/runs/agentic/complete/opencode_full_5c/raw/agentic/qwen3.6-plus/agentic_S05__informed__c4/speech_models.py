from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any
from enum import Enum


class TranscriptType(str, Enum):
    INTERIM = "interim"
    FINAL = "final"


@dataclass
class StreamRequest:
    model: str = "nova-2"
    language: str = "en"
    punctuate: bool = True
    interim_results: bool = True
    smart_format: bool = True
    encoding: str = "linear16"
    sample_rate: int = 16000
    channels: int = 1
    vad_events: bool = False
    keywords: Optional[List[str]] = None
    profanity_filter: bool = False
    diarize: bool = False
    redact: Optional[List[str]] = None
    alternatives: int = 1
    tag: Optional[List[str]] = None


@dataclass
class WordInfo:
    word: str
    start: float
    end: float
    confidence: float = 1.0
    speaker: Optional[str] = None
    punctuated_word: Optional[str] = None


@dataclass
class AlternativeResult:
    transcript: str
    confidence: float
    words: List[WordInfo] = field(default_factory=list)


@dataclass
class StreamingTranscriptResponse:
    transcript_type: TranscriptType
    alternatives: List[AlternativeResult]
    is_final: bool
    speech_final: bool
    start: float = 0.0
    duration: float = 0.0
    channel_index: int = 0
    metadata: Dict[str, Any] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None


@dataclass
class NormalizedTranscript:
    text: str
    confidence: float
    start_time: float
    end_time: float
    is_final: bool
    words: List[WordInfo] = field(default_factory=list)
    speaker: Optional[str] = None
    language: str = "en"


def parse_deepgram_response(raw: Dict[str, Any]) -> StreamingTranscriptResponse:
    channel = raw.get("channel", {})
    alternatives_raw = channel.get("alternatives", [])
    alternatives = []
    for alt in alternatives_raw:
        words = [
            WordInfo(
                word=w.get("word", ""),
                start=w.get("start", 0.0),
                end=w.get("end", 0.0),
                confidence=w.get("confidence", 1.0),
                speaker=w.get("speaker"),
                punctuated_word=w.get("punctuated_word"),
            )
            for w in alt.get("words", [])
        ]
        alternatives.append(
            AlternativeResult(
                transcript=alt.get("transcript", ""),
                confidence=alt.get("confidence", 0.0),
                words=words,
            )
        )

    is_final = raw.get("is_final", False)
    speech_final = channel.get("speech_final", False)
    transcript_type = TranscriptType.FINAL if is_final else TranscriptType.INTERIM

    return StreamingTranscriptResponse(
        transcript_type=transcript_type,
        alternatives=alternatives,
        is_final=is_final,
        speech_final=speech_final,
        start=channel.get("start", 0.0),
        duration=channel.get("duration", 0.0),
        channel_index=channel.get("channel_index", 0),
        metadata=raw.get("metadata", {}),
        raw_response=raw,
    )


def normalize_transcript(
    response: StreamingTranscriptResponse, language: str = "en"
) -> List[NormalizedTranscript]:
    results = []
    for alt in response.alternatives:
        start_time = response.start
        end_time = response.start + response.duration
        speaker = alt.words[0].speaker if alt.words else None
        normalized = NormalizedTranscript(
            text=alt.transcript,
            confidence=alt.confidence,
            start_time=start_time,
            end_time=end_time,
            is_final=response.is_final,
            words=alt.words,
            speaker=speaker,
            language=language,
        )
        results.append(normalized)
    return results


def merge_final_transcripts(
    transcripts: List[NormalizedTranscript],
) -> str:
    final_texts = [t.text for t in transcripts if t.is_final and t.text.strip()]
    return " ".join(final_texts).strip()


def extract_interim_text(response: StreamingTranscriptResponse) -> str:
    if not response.alternatives:
        return ""
    return response.alternatives[0].transcript
