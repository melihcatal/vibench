import json
from typing import Any, Dict, List, Optional

# ----- Request & Response Models (local POJOs) -----


class AudioChunk:
    def __init__(
        self, data: bytes, sample_rate: int = 16000, encoding: str = "l16"
    ) -> None:
        self.data = data  # raw PCM bytes
        self.sample_rate = sample_rate
        self.encoding = encoding

    def to_dict(self) -> Dict[str, Any]:
        return {
            "data": self.data,
            "sample_rate": self.sample_rate,
            "encoding": self.encoding,
        }


class TranscriptionResult:
    def __init__(self, final: bool, alternatives: List[Dict[str, Any]]) -> None:
        self.final = final
        self.alternatives = (
            alternatives  # list of { transcript: str, confidence: float, ... }
        )

    def to_dict(self) -> Dict[str, Any]:
        return {"final": self.final, "alternatives": self.alternatives}


# ----- Normalization Utilities -----


def normalize_event(event: Any) -> Optional[TranscriptionResult]:
    """Convert a raw event payload from a provider to our internal TranscriptionResult.

    This placeholder can be overridden per provider.
    """
    # Example: IBM Watson returns a dict with .results attribute
    if isinstance(event, dict) and "results" in event:
        formal = event["results"][-1]
        return TranscriptionResult(
            final=formal.get("final", False),
            alternatives=formal.get("alternatives", []),
        )
    return None


def serialize_result(result: TranscriptionResult) -> str:
    """Pretty‑print the normalized result as JSON for logging or downstream processing."""
    return json.dumps(result.to_dict(), indent=2)


# ----- Example Provider‑specific Helper (Watson) -----


def parse_watson_partial(event: Any) -> Optional[str]:
    """Extract the interim transcript from a Watson callback event."""
    if event and hasattr(event, "result") and event.result:
        interim = event.result[-1]
        if not interim.get("final", False):
            return interim["alternatives"][0].get("transcript", "")
    return None
