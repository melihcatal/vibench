"""Define local request, response, and normalization helpers for Streaming Speech-to-Text."""

from dataclasses import dataclass, field
from typing import Optional, List
from google.cloud.speech_v2.types import cloud_speech


@dataclass
class WordInfo:
    """Word-level information from a speech recognition result."""
    word: str = ""
    start_offset_seconds: float = 0.0
    end_offset_seconds: float = 0.0
    confidence: float = 0.0


@dataclass
class TranscriptAlternative:
    """A single alternative transcript from a recognition result."""
    text: str = ""
    confidence: float = 0.0
    words: list[WordInfo] = field(default_factory=list)


@dataclass
class StreamingSpeechResult:
    """Normalized result from a streaming speech recognition response."""
    is_final: bool = False
    stability: float = 0.0
    alternatives: list[TranscriptAlternative] = field(default_factory=list)
    language_code: str = ""

    @property
    def transcript(self) -> str:
        """Return the top alternative transcript text."""
        if self.alternatives:
            return self.alternatives[0].text
        return ""

    @property
    def confidence(self) -> float:
        """Return the confidence of the top alternative."""
        if self.alternatives:
            return self.alternatives[0].confidence
        return 0.0


@dataclass
class AudioChunk:
    """Represents a chunk of audio data for streaming."""
    data: bytes
    sample_rate: int = 16000
    channels: int = 1


def normalize_recognition_result(result: cloud_speech.SpeechRecognitionResult) -> StreamingSpeechResult:
    """Normalize a google-cloud-speech SpeechRecognitionResult into StreamingSpeechResult."""
    alternatives = []
    for alt in result.alternatives:
        words = []
        for word_info in getattr(alt, "words", []):
            start_seconds = 0.0
            end_seconds = 0.0
            if hasattr(word_info, "start_offset") and word_info.start_offset:
                start_seconds = word_info.start_offset.total_seconds()
            if hasattr(word_info, "end_offset") and word_info.end_offset:
                end_seconds = word_info.end_offset.total_seconds()
            words.append(WordInfo(
                word=word_info.word,
                start_offset_seconds=start_seconds,
                end_offset_seconds=end_seconds,
                confidence=word_info.confidence,
            ))
        alternatives.append(TranscriptAlternative(
            text=alt.transcript,
            confidence=alt.confidence,
            words=words,
        ))
    return StreamingSpeechResult(
        is_final=result.is_final,
        stability=result.stability,
        alternatives=alternatives,
        language_code=result.language_code,
    )
