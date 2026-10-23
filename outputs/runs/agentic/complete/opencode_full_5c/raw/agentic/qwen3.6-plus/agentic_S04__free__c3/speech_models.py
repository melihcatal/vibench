from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any


@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_labels: bool = False
    punctuate: bool = True
    format_text: bool = True
    dual_channel: bool = False
    word_boost: List[str] = field(default_factory=list)
    language_code: Optional[str] = None
    auto_chapters: bool = False
    auto_highlights: bool = False
    custom_spelling: List[Dict[str, Any]] = field(default_factory=list)

    def to_assemblyai_payload(self) -> dict:
        payload = {
            "audio_url": self.audio_url,
            "speaker_labels": self.speaker_labels,
            "punctuate": self.punctuate,
            "format_text": self.format_text,
            "dual_channel": self.dual_channel,
            "auto_chapters": self.auto_chapters,
            "auto_highlights": self.auto_highlights,
        }
        if self.word_boost:
            payload["word_boost"] = self.word_boost
        if self.language_code:
            payload["language_code"] = self.language_code
        if self.custom_spelling:
            payload["custom_spelling"] = self.custom_spelling
        return payload


@dataclass
class WordSegment:
    text: str
    start: int
    end: int
    confidence: float
    speaker: Optional[str] = None

    @classmethod
    def from_assemblyai_word(cls, word: dict) -> "WordSegment":
        return cls(
            text=word.get("text", ""),
            start=word.get("start", 0),
            end=word.get("end", 0),
            confidence=word.get("confidence", 0.0),
            speaker=word.get("speaker"),
        )


@dataclass
class Utterance:
    speaker: str
    text: str
    start: int
    end: int
    words: List[WordSegment] = field(default_factory=list)
    confidence: float = 0.0

    @classmethod
    def from_assemblyai_utterance(cls, utt: dict) -> "Utterance":
        words = [WordSegment.from_assemblyai_word(w) for w in utt.get("words", [])]
        return cls(
            speaker=utt.get("speaker", "unknown"),
            text=utt.get("text", ""),
            start=utt.get("start", 0),
            end=utt.get("end", 0),
            words=words,
            confidence=utt.get("confidence", 0.0),
        )


@dataclass
class TranscriptionResult:
    transcript_id: str
    status: str
    text: str = ""
    words: List[WordSegment] = field(default_factory=list)
    utterances: List[Utterance] = field(default_factory=list)
    audio_duration: float = 0.0
    confidence: float = 0.0
    chapters: List[Dict[str, Any]] = field(default_factory=list)
    summary: Optional[str] = None

    @classmethod
    def from_assemblyai_response(cls, data: dict) -> "TranscriptionResult":
        words = [WordSegment.from_assemblyai_word(w) for w in data.get("words", [])]
        utterances = [
            Utterance.from_assemblyai_utterance(u) for u in data.get("utterances", [])
        ]
        return cls(
            transcript_id=data.get("id", ""),
            status=data.get("status", ""),
            text=data.get("text", ""),
            words=words,
            utterances=utterances,
            audio_duration=data.get("audio_duration", 0.0),
            confidence=data.get("confidence", 0.0),
            chapters=data.get("chapters", []),
            summary=data.get("summary"),
        )


@dataclass
class SegmentTranslation:
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    start: int = 0
    end: int = 0


@dataclass
class ModerationResult:
    flagged: bool
    categories: Dict[str, bool] = field(default_factory=dict)
    scores: Dict[str, float] = field(default_factory=dict)
    flagged_segments: List[Dict[str, Any]] = field(default_factory=list)


@dataclass
class TranscriptSummary:
    title: str
    summary: str
    key_points: List[str] = field(default_factory=list)
    action_items: List[str] = field(default_factory=list)
    sentiment: Optional[str] = None
    word_count: int = 0
    speaker_count: int = 0


@dataclass
class SegmentEmbedding:
    text: str
    embedding: List[float]
    start: int = 0
    end: int = 0
    speaker: Optional[str] = None
