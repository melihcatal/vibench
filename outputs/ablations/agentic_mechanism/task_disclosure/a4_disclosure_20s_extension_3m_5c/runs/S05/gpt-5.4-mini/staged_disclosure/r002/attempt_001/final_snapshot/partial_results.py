import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional

import boto3


@dataclass
class RecognitionResult:
    text: str = ""
    is_final: bool = False
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    alternatives: List[Dict[str, Any]] = field(default_factory=list)


class TranscribeStreamingEventHandler:
    def __init__(self) -> None:
        self._partial_text = ""
        self._final_segments: List[str] = []

    def handle_event(self, event: Dict[str, Any]) -> RecognitionResult:
        transcript_event = event.get("TranscriptEvent")
        if not transcript_event:
            return RecognitionResult()

        results = transcript_event.get("Transcript", {}).get("Results", [])
        if not results:
            return RecognitionResult()

        latest = results[0]
        alternatives = latest.get("Alternatives", [])
        transcript = alternatives[0].get("Transcript", "") if alternatives else ""
        is_final = not latest.get("IsPartial", True)

        if is_final:
            if transcript:
                self._final_segments.append(transcript)
            self._partial_text = ""
        else:
            self._partial_text = transcript

        return RecognitionResult(
            text=self.get_full_text(),
            is_final=is_final,
            start_time=latest.get("StartTime"),
            end_time=latest.get("EndTime"),
            alternatives=alternatives,
        )

    def get_full_text(self) -> str:
        parts = list(self._final_segments)
        if self._partial_text:
            parts.append(self._partial_text)
        return " ".join(parts).strip()


def create_transcribe_client(region_name: Optional[str] = None):
    return boto3.client("transcribe", region_name=region_name or os.getenv("AWS_REGION", "us-east-1"))
