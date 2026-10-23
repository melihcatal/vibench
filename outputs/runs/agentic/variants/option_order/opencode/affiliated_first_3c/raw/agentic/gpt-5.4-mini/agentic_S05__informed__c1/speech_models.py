from dataclasses import dataclass


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    language: str = "en-US"


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def transcript_from_result(
    text: str, final: bool = False, language: str = "en-US"
) -> TranscriptChunk:
    return TranscriptChunk(
        text=normalize_transcript(text), is_final=final, language=language
    )
