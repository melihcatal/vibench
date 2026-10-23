from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Optional


@dataclass
class TranscriptChunk:
    text: str
    is_final: bool = False
    confidence: Optional[float] = None


@dataclass
class NormalizedTranscript:
    text: str
    final: bool
    confidence: Optional[float]


def normalize_transcript(text: str) -> str:
    return " ".join(text.strip().split())


def normalize_chunk(chunk: TranscriptChunk) -> NormalizedTranscript:
    return NormalizedTranscript(
        text=normalize_transcript(chunk.text),
        final=chunk.is_final,
        confidence=chunk.confidence,
    )


def response_to_chunks(response: Any) -> List[TranscriptChunk]:
    chunks: List[TranscriptChunk] = []
    for result in getattr(response, "results", []):
        if not getattr(result, "alternatives", None):
            continue
        alt = result.alternatives[0]
        chunks.append(
            TranscriptChunk(
                text=getattr(alt, "transcript", ""),
                is_final=getattr(result, "is_final", False),
                confidence=getattr(alt, "confidence", None),
            )
        )
    return chunks
