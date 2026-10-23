from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional


@dataclass
class SafetyCategoryScore:
    name: str
    score: float
    blocked: bool = False


@dataclass
class ModerationResult:
    text: str
    provider: str
    model: str
    flagged: bool
    categories: Dict[str, SafetyCategoryScore] = field(default_factory=dict)
    raw_response: Optional[Dict[str, Any]] = None

    def as_dict(self) -> Dict[str, Any]:
        return {
            "text": self.text,
            "provider": self.provider,
            "model": self.model,
            "flagged": self.flagged,
            "categories": {
                key: {
                    "name": value.name,
                    "score": value.score,
                    "blocked": value.blocked,
                }
                for key, value in self.categories.items()
            },
            "raw_response": self.raw_response,
        }


@dataclass
class RedactionSpan:
    start: int
    end: int
    category: str
    replacement: str = "[REDACTED]"


@dataclass
class BatchModerationDecision:
    index: int
    text: str
    result: ModerationResult


CATEGORY_SYNONYMS = {
    "toxicity": ["TOXICITY", "toxicity"],
    "insult": ["INSULT", "insult"],
    "threat": ["THREAT", "threat"],
    "sexual": ["SEXUALLY_EXPLICIT", "sexual", "sexual_explicit"],
    "profanity": ["PROFANITY", "profanity"],
    "identity_attack": ["IDENTITY_ATTACK", "identity_attack"],
}


def normalize_scores(provider_scores: Dict[str, Any]) -> Dict[str, SafetyCategoryScore]:
    normalized: Dict[str, SafetyCategoryScore] = {}
    for canonical_name, aliases in CATEGORY_SYNONYMS.items():
        for alias in aliases:
            if alias in provider_scores:
                value = provider_scores[alias]
                if isinstance(value, dict):
                    score = float(value.get("summaryScore", value.get("score", 0.0)))
                    blocked = bool(value.get("blocked", False))
                else:
                    score = float(value)
                    blocked = False
                normalized[canonical_name] = SafetyCategoryScore(
                    name=canonical_name,
                    score=score,
                    blocked=blocked,
                )
                break
    return normalized


def merge_text_spans(text: str, spans: List[RedactionSpan]) -> str:
    if not spans:
        return text
    ordered = sorted(spans, key=lambda span: (span.start, span.end))
    parts: List[str] = []
    cursor = 0
    for span in ordered:
        start = max(0, min(len(text), span.start))
        end = max(start, min(len(text), span.end))
        if start < cursor:
            continue
        parts.append(text[cursor:start])
        parts.append(span.replacement)
        cursor = end
    parts.append(text[cursor:])
    return "".join(parts)
