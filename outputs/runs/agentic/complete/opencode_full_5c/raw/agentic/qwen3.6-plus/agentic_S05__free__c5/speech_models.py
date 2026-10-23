from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
from datetime import datetime


@dataclass
class WordInfo:
    word: str
    start_offset_ms: float = 0.0
    end_offset_ms: float = 0.0
    confidence: float = 0.0
    speaker_tag: int = 0


@dataclass
class TranscriptAlternative:
    text: str
    confidence: float = 0.0
    words: List[WordInfo] = field(default_factory=list)


@dataclass
class StreamingRecognitionResult:
    is_final: bool
    alternatives: List[TranscriptAlternative]
    language_code: str = ""
    result_end_offset_ms: float = 0.0
    channel_tag: int = 0


@dataclass
class StreamingTranscriptEvent:
    result: StreamingRecognitionResult
    timestamp: datetime = field(default_factory=datetime.utcnow)

    @property
    def is_interim(self) -> bool:
        return not self.result.is_final

    @property
    def text(self) -> str:
        if self.result.alternatives:
            return self.result.alternatives[0].text
        return ""

    @property
    def confidence(self) -> float:
        if self.result.alternatives:
            return self.result.alternatives[0].confidence
        return 0.0


@dataclass
class StreamingRequest:
    recognizer: str
    config: Any
    audio_content: bytes = b""
    streaming_features: Optional[Dict[str, Any]] = None


def normalize_word_info(raw_word: Any) -> WordInfo:
    start_ms = 0.0
    end_ms = 0.0
    if hasattr(raw_word, "start_offset"):
        start_ms = raw_word.start_offset.total_seconds() * 1000
    if hasattr(raw_word, "end_offset"):
        end_ms = raw_word.end_offset.total_seconds() * 1000
    return WordInfo(
        word=getattr(raw_word, "word", ""),
        start_offset_ms=start_ms,
        end_offset_ms=end_ms,
        confidence=getattr(raw_word, "confidence", 0.0),
        speaker_tag=getattr(raw_word, "speaker_tag", 0),
    )


def normalize_alternative(raw_alt: Any) -> TranscriptAlternative:
    words = []
    if hasattr(raw_alt, "words"):
        words = [normalize_word_info(w) for w in raw_alt.words]
    return TranscriptAlternative(
        text=getattr(raw_alt, "transcript", ""),
        confidence=getattr(raw_alt, "confidence", 0.0),
        words=words,
    )


def normalize_recognition_result(raw_result: Any) -> StreamingRecognitionResult:
    alternatives = []
    if hasattr(raw_result, "alternatives"):
        alternatives = [normalize_alternative(a) for a in raw_result.alternatives]
    end_offset_ms = 0.0
    if hasattr(raw_result, "result_end_offset"):
        end_offset_ms = raw_result.result_end_offset.total_seconds() * 1000
    return StreamingRecognitionResult(
        is_final=getattr(raw_result, "is_final", False),
        alternatives=alternatives,
        language_code=getattr(raw_result, "language_code", ""),
        result_end_offset_ms=end_offset_ms,
        channel_tag=getattr(raw_result, "channel_tag", 0),
    )


def normalize_streaming_event(raw_response: Any) -> Optional[StreamingTranscriptEvent]:
    if not hasattr(raw_response, "results"):
        return None
    results = raw_response.results
    if not results:
        return None
    latest = results[-1]
    result = normalize_recognition_result(latest)
    return StreamingTranscriptEvent(result=result)


def merge_final_transcripts(events: List[StreamingTranscriptEvent]) -> str:
    final_texts = []
    for event in events:
        if event.result.is_final and event.text:
            final_texts.append(event.text)
    return " ".join(final_texts).strip()


def extract_interim_text(event: StreamingTranscriptEvent) -> str:
    if event.is_interim:
        return event.text
    return ""
