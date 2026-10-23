import dataclasses

@dataclasses.dataclass
class TranscriptionRequest:
    audio_file_url: str
    locale: str = "en-US"
    display_name: str = "BatchTranscriptionJob"

@dataclasses.dataclass
class TranscriptionResult:
    id: str
    status: str
    transcript_url: str | None = None
    error_message: str | None = None
