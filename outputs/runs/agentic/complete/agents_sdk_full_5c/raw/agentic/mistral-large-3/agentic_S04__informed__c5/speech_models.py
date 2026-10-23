from typing import List, Dict, Any, Optional
from dataclasses import dataclass

@dataclass
class TranscriptionRequest:
    audio: Any
    language_code: str
    speaker_labels: bool = True
    
    def to_assemblyai_dict(self) -> Dict[str, Any]:
        return {
            "audio": self.audio,
            "language_code": self.language_code,
            "speaker_labels": self.speaker_labels
        }

@dataclass
class DiarizationResult:
    utterances: List[Dict[str, Any]]
    
    @classmethod
    def from_assemblyai_utterances(cls, utterances: List[Any]) -> "DiarizationResult":
        return cls(utterances=[{
            "speaker": u.speaker,
            "text": u.text,
            "start": u.start,
            "end": u.end
        } for u in utterances])

@dataclass
class TimestampedTranscript:
    words: List[Dict[str, Any]]
    
    @classmethod
    def from_assemblyai_words(cls, words: List[Any]) -> "TimestampedTranscript":
        return cls(words=[{
            "text": w.text,
            "start": w.start,
            "end": w.end
        } for w in words])