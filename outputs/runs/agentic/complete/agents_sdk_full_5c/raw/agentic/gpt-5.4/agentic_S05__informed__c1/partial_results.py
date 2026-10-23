from __future__ import annotations

from typing import Dict, List, Tuple

from speech_models import StreamingTranscriptChunk, normalize_transcript_text


class PartialResultHandler:
    def __init__(self) -> None:
        self._latest_partial: str = ""
        self._finalized: List[str] = []

    def consume(self, chunk: StreamingTranscriptChunk) -> Dict[str, object]:
        text = normalize_transcript_text(chunk.text)
        if chunk.is_final:
            if text:
                self._finalized.append(text)
            self._latest_partial = ""
        else:
            self._latest_partial = text
        return {
            "display_text": self.current_display_text(),
            "is_final": chunk.is_final,
            "confidence": chunk.confidence,
            "provider": "Deepgram",
            "model": chunk.raw.get("metadata", {}).get("model_info", {}).get("name", "nova-2"),
        }

    def current_display_text(self) -> str:
        parts = [*self._finalized]
        if self._latest_partial:
            parts.append(self._latest_partial)
        return normalize_transcript_text(" ".join(parts))

    def snapshot(self) -> Tuple[List[str], str]:
        return list(self._finalized), self._latest_partial
