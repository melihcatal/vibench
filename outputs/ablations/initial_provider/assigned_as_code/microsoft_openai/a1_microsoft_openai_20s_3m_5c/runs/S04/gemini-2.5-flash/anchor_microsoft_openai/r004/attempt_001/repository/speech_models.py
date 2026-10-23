import dataclasses
import typing


@dataclasses.dataclass
class TranscriptionConfig:
    audio_uri: str
    language_code: str
    diarization_enabled: bool = False
    word_level_timestamps_enabled: bool = False
    display_name: str = "transcription_job"


@dataclasses.dataclass
class TranscriptionResult:
    job_id: str
    status: str
    transcript: typing.Optional[str] = None
    word_timestamps: typing.Optional[typing.List[typing.Dict]] = None
    speaker_segments: typing.Optional[typing.List[typing.Dict]] = None


@dataclasses.dataclass
class TranslatedSegment:
    segment_id: int
    text: str
    translated_text: str
    source_language: str
    target_language: str


@dataclasses.dataclass
class ModerationResult:
    segment_id: int
    text: str
    flagged: bool
    categories: typing.List[str]


@dataclasses.dataclass
class SummaryResult:
    summary: str


@dataclasses.dataclass
class EmbeddingResult:
    segment_id: int
    text: str
    embedding: typing.List[float]
