import dataclasses

@dataclasses.dataclass
class SpeechRecognitionRequest:
    audio_chunks: list[bytes]
    sample_rate_hz: int
    language_code: str
    enable_automatic_punctuation: bool = False

def normalize_transcript(transcript: str) -> str:
    return transcript.strip()
