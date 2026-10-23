from dataclasses import dataclass
from typing import Optional, Dict, Any

@dataclass
class TranscriptionRequest:
    audio_file: Any
    language_code: Optional[str] = None
    speaker_labels: bool = False
    word_timestamps: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "audio": self.audio_file,
            "language_code": self.language_code,
            "speaker_labels": self.speaker_labels,
            "word_timestamps": self.word_timestamps
        }

@dataclass
class DiarizationRequest:
    transcript_id: str
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript_id": self.transcript_id,
            "speaker_labels": True
        }