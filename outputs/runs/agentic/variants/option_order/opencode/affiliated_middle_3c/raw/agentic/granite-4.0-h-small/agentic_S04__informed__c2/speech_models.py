import os
from typing import Dict, List
from pathlib import Path

# Define request/response models and normalization utilities for Batch Speech-to-Text

ASSEMBLYAI_API_KEY = os.getenv("ASSEMBLYAI_API_KEY")
if not ASSEMBLYAI_API_KEY:
    raise RuntimeError("ASSEMBLYAI_API_KEY environment variable not set")

# Simple Response model for a completed transcription job


class TranscriptionResult:
    def __init__(self, data: Dict):
        self.id = data.get("id")
        self.text = data.get("text")
        self.status = data.get("status")
        self.words = [] if data.get("words") is None else data["words"]

    def __repr__(self):
        return f"TranscriptionResult(id={self.id}, status={self.status}, len_words={len(self.words)})"


# Normalization helper: ensure word objects contain text, start, end


def normalize_words(words: List[Dict]) -> List[Dict]:
    normalized = []
    for w in words:
        normalized.append(
            {
                "text": w.get("text", ""),
                "start_sec": w.get("start"),
                "end_sec": w.get("end"),
            }
        )
    return normalized


# Request payload normalizer for batch transcription


def build_transcription_payload(audio_url: str, options: dict = None) -> dict:
    options = options or {}
    return {
        "audio_url": audio_url,
        "config": {
            "auto_punctuation": options.get("auto_punctuation", True),
            "format_text": options.get("format_text", True),
            **options.get("extra", {}),
        },
    }


# Helper to validate required env vars


def validate_env() -> None:
    required = ["ASSEMBLYAI_API_KEY"]
    missing = [v for v in required if not os.getenv(v)]
    if missing:
        raise RuntimeError(f"Missing environment variables: {missing}")


validate_env()
