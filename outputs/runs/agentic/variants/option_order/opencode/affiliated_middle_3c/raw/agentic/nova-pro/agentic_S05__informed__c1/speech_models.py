from typing import Any, Dict


def normalize_transcript(transcript: Dict[str, Any]) -> str:
    return transcript["results"][0]["alternatives"][0]["transcript"]
