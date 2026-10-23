import dataclasses

@dataclasses.dataclass
class TranscriptionRequest:
    audio_file_uri: str
    language_code: str = "en-US"
    job_name: str = ""

@dataclasses.dataclass
class TranscriptionResult:
    job_name: str
    status: str
    transcript_uri: str = ""
    transcript_text: str = ""
    segments: list = dataclasses.field(default_factory=list)

@dataclasses.dataclass
class DiarizationRequest:
    audio_file_uri: str
    language_code: str = "en-US"
    job_name: str = ""

@dataclasses.dataclass
class TimestampRequest:
    job_name: str

@dataclasses.dataclass
class TranslationRequest:
    text: str
    source_language: str
    target_language: str

@dataclasses.dataclass
class ModerationRequest:
    text: str

@dataclasses.dataclass
class SummaryRequest:
    text: str

@dataclasses.dataclass
class EmbeddingRequest:
    text_segments: list[str]
