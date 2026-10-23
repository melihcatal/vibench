import os
from typing import Any, Dict, Iterable, List, Optional, Union

from openai import OpenAI


def _client() -> OpenAI:
    return OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


def transcribe_with_timestamps(audio_path: str, timestamp_granularities: Optional[Iterable[str]] = None) -> Dict[str, Any]:
    client = _client()
    with open(audio_path, "rb") as audio_file:
        response = client.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file,
            response_format="verbose_json",
            timestamp_granularities=list(timestamp_granularities) if timestamp_granularities is not None else ["word", "segment"],
        )
    if hasattr(response, "model_dump"):
        return response.model_dump()
    return dict(response)


def get_timestamps(transcription_result: Dict[str, Any]) -> Dict[str, List[Dict[str, Any]]]:
    words = transcription_result.get("words") or []
    segments = transcription_result.get("segments") or []
    return {"words": words, "segments": segments}


def word_timestamps(transcription_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(transcription_result.get("words") or [])


def segment_timestamps(transcription_result: Dict[str, Any]) -> List[Dict[str, Any]]:
    return list(transcription_result.get("segments") or [])


def extract_timestamps(transcription_result: Dict[str, Any], kind: str = "word") -> List[Dict[str, Any]]:
    if kind == "word":
        return word_timestamps(transcription_result)
    if kind == "segment":
        return segment_timestamps(transcription_result)
    raise ValueError("kind must be 'word' or 'segment'")
