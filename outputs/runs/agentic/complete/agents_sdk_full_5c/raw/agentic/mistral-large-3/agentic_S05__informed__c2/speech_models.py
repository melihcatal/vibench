from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class TranscriptEvent:
    transcript: str
    is_final: bool
    confidence: float = 0.0

    @classmethod
    def from_deepgram(cls, event: Dict[str, Any]) -> "TranscriptEvent":
        if "channel" not in event or "alternatives" not in event["channel"]:
            return None
        alternative = event["channel"]["alternatives"][0]
        return cls(
            transcript=alternative.get("transcript", ""),
            is_final=event.get("is_final", False),
            confidence=alternative.get("confidence", 0.0)
        )