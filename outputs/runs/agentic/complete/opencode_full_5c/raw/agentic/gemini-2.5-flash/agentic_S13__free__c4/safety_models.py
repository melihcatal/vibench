from dataclasses import dataclass, field
from typing import List, Dict, Optional


@dataclass
class ModerationRequest:
    """Represents a request for text moderation."""

    text_content: str
    language_code: str = "en"


@dataclass
class ModerationCategoryScore:
    """Represents a single moderation category score."""

    name: str
    score: float


@dataclass
class ModerationResponse:
    """Represents the response from a text moderation service."""

    processed_text: str
    scores: List[ModerationCategoryScore] = field(default_factory=list)
    is_unsafe: bool = False
    denial_reasons: List[str] = field(default_factory=list)

    def to_dict(self) -> Dict:
        return {
            "processed_text": self.processed_text,
            "scores": [{"name": s.name, "score": s.score} for s in self.scores],
            "is_unsafe": self.is_unsafe,
            "denial_reasons": self.denial_reasons,
        }

    @staticmethod
    def from_dict(data: Dict) -> "ModerationResponse":
        scores = [
            ModerationCategoryScore(name=s["name"], score=s["score"])
            for s in data.get("scores", [])
        ]
        return ModerationResponse(
            processed_text=data.get("processed_text", ""),
            scores=scores,
            is_unsafe=data.get("is_unsafe", False),
            denial_reasons=data.get("denial_reasons", []),
        )


@dataclass
class RedactionRequest:
    """Represents a request for text redaction."""

    text_content: str
    info_types: Optional[List[str]] = None


@dataclass
class RedactionResponse:
    """Represents the response from a text redaction service."""

    original_text: str
    redacted_text: str
    redaction_applied: bool


if __name__ == "__main__":
    # Example usage
    mod_request = ModerationRequest(text_content="This is a test message.")
    print(f"Moderation Request: {mod_request}")

    mod_scores = [
        ModerationCategoryScore(name="TOXICITY", score=0.1),
        ModerationCategoryScore(name="SEXUAL", score=0.05),
    ]
    mod_response = ModerationResponse(
        processed_text="This is a test message.", scores=mod_scores, is_unsafe=False
    )
    print(f"Moderation Response: {mod_response}")
    print(f"Moderation Response Dict: {mod_response.to_dict()}")

    red_request = RedactionRequest(text_content="My email is test@example.com.")
    print(f"Redaction Request: {red_request}")
