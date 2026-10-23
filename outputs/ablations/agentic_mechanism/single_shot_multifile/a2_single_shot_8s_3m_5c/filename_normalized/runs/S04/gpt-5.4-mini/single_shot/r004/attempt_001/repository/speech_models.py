from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class AudioSource:
    url: Optional[str] = None
    file_path: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        data: Dict[str, Any] = {}
        if self.url:
            data['url'] = self.url
        if self.file_path:
            data['file_path'] = self.file_path
        return data


@dataclass
class TranscriptionRequest:
    audio_source: AudioSource
    language: Optional[str] = None
    model: Optional[str] = None
    webhook_url: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

    def to_dict(self) -> Dict[str, Any]:
        data = {'audio_source': self.audio_source.to_dict()}
        if self.language:
            data['language'] = self.language
        if self.model:
            data['model'] = self.model
        if self.webhook_url:
            data['webhook_url'] = self.webhook_url
        if self.metadata:
            data['metadata'] = self.metadata
        return data


@dataclass
class DiarizedTranscriptionRequest(TranscriptionRequest):
    speakers: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        data = super().to_dict()
        if self.speakers is not None:
            data['speakers'] = self.speakers
        data['speaker_labels'] = True
        return data


@dataclass
class TimestampedTranscriptRequest:
    job_id: str
    granularity: str = 'word'
    include_confidence: bool = False


@dataclass
class TranscriptionSubmission:
    id: str
    status: str
    transcript: Optional[str] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'status': self.status, 'transcript': self.transcript, 'raw': self.raw}


@dataclass
class TranscriptionJob:
    id: str
    status: str
    transcript: Optional[str] = None
    words: Optional[List[Dict[str, Any]]] = None
    segments: Optional[List[Dict[str, Any]]] = None
    raw: Dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return {'id': self.id, 'status': self.status, 'transcript': self.transcript, 'words': self.words, 'segments': self.segments, 'raw': self.raw}


def normalize_timestamps(result: Any) -> Dict[str, Any]:
    if isinstance(result, dict):
        if 'words' in result or 'segments' in result:
            return result
        return {'result': result}
    if hasattr(result, 'to_dict'):
        return result.to_dict()
    return {'result': result}
