from dataclasses import dataclass, field
from typing import Dict, Any, List

@dataclass
class SafetyDecision:
    flagged: bool
    categories: Dict[str, float]
    details: Dict[str, Any] = field(default_factory=dict)

def normalize_openai_result(result: dict) -> SafetyDecision:
    categories = {k: v.get('true', 0.0) for k, v in result.get('category_scores', {}).items()}
    flagged = result.get('flagged', any(categories.values()))
    return SafetyDecision(flagged=flagged, categories=categories)

def normalize_perspective_result(response: dict) -> SafetyDecision:
    categories = {}
    for attr in response.get('attributeScores', []):
        attr_name = list(attr['name'].keys())[0]
        score_value = attr['summaryScore']['score']['value']
        categories[attr_name] = score_value
    flagged = any(score > 0.5 for score in categories.values())
    return SafetyDecision(flagged=flagged, categories=categories)
