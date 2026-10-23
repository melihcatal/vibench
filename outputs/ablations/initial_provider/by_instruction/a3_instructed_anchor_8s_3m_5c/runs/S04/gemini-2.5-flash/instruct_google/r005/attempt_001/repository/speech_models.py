from dataclasses import dataclass

@dataclass
class TranscriptionRequest:
    audio_uri: str
    language_code: str = "en-US"
    enable_speaker_diarization: bool = False
    enable_word_time_offsets: bool = False

@dataclass
class TranscriptionResult:
    transcript: str
    word_timestamps: list = None
    diarization_speakers: list = None
