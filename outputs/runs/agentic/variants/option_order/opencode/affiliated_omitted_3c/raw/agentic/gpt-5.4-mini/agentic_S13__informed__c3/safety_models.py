import re
from dataclasses import dataclass
from typing import Any, Dict, Iterable, List, Mapping, Optional

DEFAULT_CATEGORIES = ("toxicity", "insult", "threat", "profanity", "sexual", "identity_attack")

@dataclass
class ModerationDecision:
    allowed: bool
    scores: Dict[str, float]
    raw: Dict[str, Any]


def normalize_text(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").strip())


def normalize_thresholds(thresholds: Optional[Mapping[str, float]]) -> Dict[str, float]:
    base = {name: 0.5 for name in DEFAULT_CATEGORIES}
    if thresholds:
        for key, value in thresholds.items():
            base[str(key)] = float(value)
    return base


def to_message_list(messages: Iterable[str]) -> List[str]:
    return [normalize_text(m) for m in messages]
