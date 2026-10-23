
from dataclasses import dataclass
from typing import List, Dict, Any

@dataclass
class SafetyRequest:
    text_content: str

@dataclass
class SafetyCategory:
    category: str
    score: float

@dataclass
class SafetyResponse:
    id: str
    categories: List[SafetyCategory]
    overall_verdict: str

def normalize_scores(scores: Dict[str, Any]) -> Dict[str, float]:
    """
    Normalizes a dictionary of scores. This is a placeholder and
    should be replaced with actual normalization logic based on the model's output.
    """
    normalized_results = {}
    for category, score_info in scores.items():
        # Assuming score_info is a dict with a 'score' key or directly the score
        if isinstance(score_info, dict) and 'score' in score_info:
            normalized_results[category] = float(score_info['score'])
        else:
            normalized_results[category] = float(score_info)
    return normalized_results
