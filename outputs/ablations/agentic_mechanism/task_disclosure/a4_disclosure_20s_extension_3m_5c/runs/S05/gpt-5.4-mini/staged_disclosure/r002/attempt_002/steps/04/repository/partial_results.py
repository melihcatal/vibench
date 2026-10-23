from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import assemblyai as aai


@dataclass
class RecognitionEvent:
    text: str
    is_final: bool
    confidence: Optional[float] = None
    words: Optional[List[Dict[str, Any]]] = None


class PartialResultsHandler:
    def __init__(self, api_key: Optional[str] = None) -> None:
        self.api_key = api_key or os.environ.get("ASSEMBLYAI_API_KEY")
        if not self.api_key:
            raise ValueError("ASSEMBLYAI_API_KEY is required")
        aai.settings.api_key = self.api_key

    def handle_event(self, event: Dict[str, Any]) -> RecognitionEvent:
        text = str(event.get("text", "")).strip()
        is_final = bool(event.get("message_type") == "FinalTranscript" or event.get("is_final"))
        confidence = event.get("confidence")
        words = event.get("words")
        return RecognitionEvent(text=text, is_final=is_final, confidence=confidence, words=words)

    def process_stream(self, stream: Any) -> List[RecognitionEvent]:
        results: List[RecognitionEvent] = []
        for event in stream:
            results.append(self.handle_event(event))
        return results


def build_assemblyai_transcriber(sample_rate: int = 16000) -> aai.RealtimeTranscriber:
    return aai.RealtimeTranscriber(sample_rate=sample_rate)
