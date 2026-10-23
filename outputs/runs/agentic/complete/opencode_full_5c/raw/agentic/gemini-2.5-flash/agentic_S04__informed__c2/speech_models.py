from dataclasses import dataclass


@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_diarization: bool = False
    word_boost: list[str] | None = None


@dataclass
class TranscriptionResponse:
    id: str
    status: str
    text: str | None = None
    words: list[dict] | None = None
    utterances: list[dict] | None = None
