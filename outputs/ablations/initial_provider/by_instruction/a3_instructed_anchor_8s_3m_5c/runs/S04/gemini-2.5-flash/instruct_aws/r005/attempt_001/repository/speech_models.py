from dataclasses import dataclass

@dataclass
class TranscriptionJobRequest:
    job_name: str
    audio_file_uri: str
    media_format: str  # e.g., "wav", "mp3", "flac"
    language_code: str # e.g., "en-US", "es-ES"

@dataclass
class TranscriptionJobResult:
    job_name: str
    status: str
    transcript_file_uri: str | None = None
    failure_reason: str | None = None
