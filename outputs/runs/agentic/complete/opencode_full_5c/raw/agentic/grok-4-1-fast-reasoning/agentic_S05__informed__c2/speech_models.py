from dataclasses import dataclass


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool
