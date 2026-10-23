from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Sequence, Union

import os

from openai import OpenAI


@dataclass
class TimestampSpan:
    start: float
    end: float
    text: str


class TimestampedTranscript:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.client = OpenAI(api_key=api_key or os.environ.get("OPENAI_API_KEY"))

    def transcribe(self, audio_file_path: str, timestamp_granularities: Sequence[str] = ("word",)) -> Dict[str, Any]:
        with open(audio_file_path, "rb") as audio_file:
            response = self.client.audio.transcriptions.create(
                model="gpt-4o-transcribe",
                file=audio_file,
                response_format="verbose_json",
                timestamp_granularities=list(timestamp_granularities),
            )
        return response.model_dump() if hasattr(response, "model_dump") else dict(response)

    @staticmethod
    def extract_word_timestamps(transcription_result: Dict[str, Any]) -> List[TimestampSpan]:
        words = transcription_result.get("words", []) or []
        return [
            TimestampSpan(start=float(word["start"]), end=float(word["end"]), text=str(word["word"]))
            for word in words
            if "start" in word and "end" in word and "word" in word
        ]

    @staticmethod
    def extract_segment_timestamps(transcription_result: Dict[str, Any]) -> List[TimestampSpan]:
        segments = transcription_result.get("segments", []) or []
        return [
            TimestampSpan(start=float(segment["start"]), end=float(segment["end"]), text=str(segment.get("text", "")))
            for segment in segments
            if "start" in segment and "end" in segment
        ]

    @classmethod
    def timestamps_for(cls, transcription_result: Dict[str, Any], granularity: str = "word") -> List[TimestampSpan]:
        if granularity == "segment":
            return cls.extract_segment_timestamps(transcription_result)
        return cls.extract_word_timestamps(transcription_result)
