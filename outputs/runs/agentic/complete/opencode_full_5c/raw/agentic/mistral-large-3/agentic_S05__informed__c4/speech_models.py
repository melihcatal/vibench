from typing import Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class SpeechEvent:
    """Normalized speech recognition event for DashScope."""

    text: str
    is_final: bool
    confidence: Optional[float] = None
    start_time: Optional[float] = None
    end_time: Optional[float] = None
    language: Optional[str] = None


class SpeechNormalizer:
    """Normalize DashScope ASR responses into consistent events."""

    @staticmethod
    def normalize_result(result: Dict[str, Any]) -> SpeechEvent:
        """Convert DashScope ASR result into a normalized event."""
        output = result.get("output", {})
        text = output.get("text", "")
        is_final = output.get("finish", False)
        confidence = output.get("confidence")
        return SpeechEvent(text=text, is_final=is_final, confidence=confidence)
