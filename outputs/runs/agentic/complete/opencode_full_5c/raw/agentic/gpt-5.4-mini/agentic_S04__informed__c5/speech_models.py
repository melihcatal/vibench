from dataclasses import dataclass


def normalize_transcript(payload):
    if not payload:
        return {"id": None, "status": None, "text": "", "segments": [], "words": []}
    return {
        "id": payload.get("id"),
        "status": payload.get("status"),
        "text": payload.get("text", ""),
        "segments": payload.get("utterances", payload.get("segments", [])) or [],
        "words": payload.get("words", []) or [],
        "audio_url": payload.get("audio_url"),
    }


@dataclass
class TranscriptionRequest:
    audio_url: str
    speaker_labels: bool = False
    word_boost: list | None = None


@dataclass
class TranslationRequest:
    text: str
    target_language: str


@dataclass
class ModerationRequest:
    text: str


@dataclass
class EmbeddingRequest:
    texts: list
