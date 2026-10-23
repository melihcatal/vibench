from typing import Dict, List
from safety_models import CategoryScore

DEFAULT_THRESHOLDS: Dict[str, float] = {
    "hate": 0.5,
    "toxicity": 0.5,
    "sexual": 0.5,
    "violence": 0.5,
    "self_harm": 0.5,
    "profanity": 0.5,
    "threat": 0.5,
    "insult": 0.5,
    "identity_attack": 0.5,
    "sexually_explicit": 0.5,
}


def compute_rationale(scores: List[CategoryScore], blocked: bool) -> str:
    if not blocked:
        return "Content deemed safe across all categories."
    high_risks = [s.category for s in scores if s.severity > 0.6]
    return f"Blocked due to high risk categories: {', '.join(high_risks)}."
