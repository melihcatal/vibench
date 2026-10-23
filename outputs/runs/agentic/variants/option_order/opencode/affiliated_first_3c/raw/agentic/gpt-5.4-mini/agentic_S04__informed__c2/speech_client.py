import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional


@dataclass
class SpeechConfig:
    api_key: str
    region: str
    language: str = "en-US"
    audio_url: Optional[str] = None


def load_speech_config() -> SpeechConfig:
    return SpeechConfig(
        api_key=os.environ.get("AZURE_SPEECH_KEY", ""),
        region=os.environ.get("AZURE_SPEECH_REGION", ""),
        language=os.environ.get("SPEECH_LANGUAGE", "en-US"),
        audio_url=os.environ.get("SPEECH_AUDIO_URL"),
    )


def normalize_segments(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    normalized = []
    for segment in segments:
        normalized.append({
            "start": segment.get("start", segment.get("offset", 0)),
            "duration": segment.get("duration", 0),
            "text": segment.get("text", ""),
            "speaker": segment.get("speaker", segment.get("speaker_label")),
            "words": segment.get("words", []),
        })
    return normalized
