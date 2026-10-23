from dataclasses import dataclass

@dataclass
class TranscriptionResult:
    text: str
    is_final: bool

@dataclass
class AudioChunk:
    content: bytes

