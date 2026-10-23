from typing import TypedDict, List, Dict, Any


class Word(TypedDict):
    text: str
    start: float
    end: float
    confidence: float


class Utterance(TypedDict):
    text: str
    speaker: str
    start: float
    end: float


class TranscriptResult(TypedDict):
    id: str
    text: str
    words: List[Word]
    utterances: List[Utterance]


def normalize_transcript(transcript: Any) -> TranscriptResult:
    words = []
    if hasattr(transcript, "words") and transcript.words:
        for w in transcript.words:
            words.append(
                {
                    "text": w.text,
                    "start": float(w.start),
                    "end": float(w.end),
                    "confidence": float(getattr(w, "confidence", 0.0)),
                }
            )
    utterances = []
    if hasattr(transcript, "utterances") and transcript.utterances:
        for u in transcript.utterances:
            utterances.append(
                {
                    "text": u.text,
                    "speaker": u.speaker,
                    "start": float(u.start),
                    "end": float(u.end),
                }
            )
    return {
        "id": getattr(transcript, "id", ""),
        "text": getattr(transcript, "text", ""),
        "words": words,
        "utterances": utterances,
    }
