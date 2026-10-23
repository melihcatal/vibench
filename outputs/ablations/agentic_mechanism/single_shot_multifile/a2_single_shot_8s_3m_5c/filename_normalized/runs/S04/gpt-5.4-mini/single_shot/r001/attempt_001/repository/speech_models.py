from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class TranscriptionSegment:
    start: Optional[float] = None
    end: Optional[float] = None
    text: str = ""
    speaker: Optional[str] = None
    words: List[Dict[str, Any]] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "TranscriptionSegment":
        return cls(start=data.get("start"), end=data.get("end"), text=data.get("text", ""), speaker=data.get("speaker"), words=data.get("words", []) or [])


@dataclass
class TranscriptionJob
    :
    id: str
    status: str
    transcript: Optional[str] = None
    segments: List[TranscriptionSegment] = field(default_factory=list)
    language: Optional[str] = None

    @property
    def is_finished(self) -> bool:
        return self.status in {"completed", "succeeded", "done"}

    @property
    def is_failed(self) -> bool:
        return self.status in {"failed", "error", "cancelled"}

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "TranscriptionJob":
        return cls(id=str(data.get("id", "")), status=str(data.get("status", "")), transcript=data.get("transcript") or data.get("text"), segments=[TranscriptionSegment.from_api(s) for s in data.get("segments", []) or []], language=data.get("language"))

    def to_result(self) -> "TranscriptionResult":
        return TranscriptionResult(id=self.id, text=self.transcript or "", segments=self.segments, language=self.language)


@dataclass
class TranscriptionResult:
    id: str
    text: str
    segments: List[TranscriptionSegment] = field(default_factory=list)
    language: Optional[str] = None

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "TranscriptionResult":
        return cls(id=str(data.get("id", "")), text=data.get("text") or data.get("transcript") or "", segments=[TranscriptionSegment.from_api(s) for s in data.get("segments", []) or []], language=data.get("language"))


@dataclass
class DiarizationRequest:
    audio_path: str
    speakers: int
    language: Optional[str] = None
    model: Optional[str] = "gpt-4o-transcribe"

    def to_form_data(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"model": self.model, "speaker_labels": "true", "speaker_count": str(self.speakers)}
        if self.language:
            data["language"] = self.language
        return data


@dataclass
class DiarizedTranscript:
    segments: List[TranscriptionSegment]
    text: str = ""

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "DiarizedTranscript":
        segments = [TranscriptionSegment.from_api(s) for s in data.get("segments", []) or []]
        return cls(segments=segments, text=data.get("text") or data.get("transcript") or "")


@dataclass
class TimestampedTranscript:
    text: str
    segments: List[TranscriptionSegment] = field(default_factory=list)

    @classmethod
    def from_api(cls, data: Dict[str, Any]) -> "TimestampedTranscript":
        return cls(text=data.get("text") or data.get("transcript") or "", segments=[TranscriptionSegment.from_api(s) for s in data.get("segments", []) or []])


@dataclass
class SubmitTranscriptionRequest:
    audio_path: str
    language: Optional[str] = None
    model: Optional[str] = "gpt-4o-transcribe"
    callback_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_form_data(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {"model": self.model}
        if self.language:
            data["language"] = self.language
        if self.callback_url:
            data["callback_url"] = self.callback_url
        if self.metadata:
            for k, v in self.metadata.items():
                data[f"metadata[{k}]"] = str(v)
        return data
