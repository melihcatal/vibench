from __future__ import annotations

from typing import Iterable, List

from speech_models import StreamingUtterance, normalize_caption


class PartialResultBuffer:
    def __init__(self) -> None:
        self._last_partial: str = ""
        self._final_segments: List[str] = []

    def handle(self, event: object) -> StreamingUtterance:
        text = normalize_caption(getattr(event, "text", "") or getattr(event, "transcript", ""))
        is_final = bool(getattr(event, "is_final", False))
        if is_final and text:
            self._final_segments.append(text)
            self._last_partial = ""
        else:
            self._last_partial = text
        return StreamingUtterance(text=text, is_final=is_final, confidence=getattr(event, "confidence", None))

    @property
    def final_text(self) -> str:
        parts: Iterable[str] = [*self._final_segments, self._last_partial]
        return normalize_caption(" ".join(p for p in parts if p))
