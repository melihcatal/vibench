from typing import Any


def normalize_transcript(transcript: Any) -> str:
    return str(transcript)


def format_response(response: Any) -> dict:
    return {"transcript": normalize_transcript(response)}
