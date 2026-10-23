# safety_models.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ModerationRequest:
    text: str
    language: Optional[str] = None

class UnsafeSpan:
    start: int
    end: int

@dataclass
class ModerationResponse:
    text: str
    language: str
    scores: Dict[str, float]  # e.g., {"toxicity": 0.73, "profanity": 0.01}
    unsafe_spans: List[UnsafeSpan] = None
    decision: Optional[str] = None  # e.g., "ALLOW", "REJECT"

    def to_dict(self) -> dict:
        return {
            "text": self.text,
            "language": self.language,
            "scores": self.scores,
            "unsafe_spans": [[s.start, s.end] for s in self.unsafe_spans] if self.unsafe_spans else [],
            "decision": self.decision,
        }

if __name__ == "__main__":
    # Example of constructing a response for demonstration.
    resp = ModerationResponse(
        text="You are an idiot.",
        language="en",
        scores={"toxicity": 0.85, "profanity": 0.02},
        unsafe_spans=[UnsafeSpan(start=3, end=7)],
        decision="REJECT",
    )
    print(resp.to_dict())
