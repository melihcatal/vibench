from typing import Dict, Any, Optional
from pydantic import BaseModel

class SafetyResult(BaseModel):
    input_text: str
    flagged: bool
    categories: Dict[str, float]
    details: Optional[str] = None

def normalize_openai(raw: Dict[str, Any], input_text: str) -> SafetyResult:
    result = raw['results'][0]
    return SafetyResult(
        input_text=input_text,
        flagged=result['flagged'],
        categories=result['category_scores']
    )

def normalize_perspective(raw: Dict[str, Any], input_text: str) -> SafetyResult:
    attribute_scores = raw.get('attributeScores', {})
    categories = {k: v['summaryScore']['value'] for k, v in attribute_scores.items()}
    flagged = max(categories.values(), default=0.0) > 0.5
    return SafetyResult(
        input_text=input_text,
        flagged=flagged,
        categories=categories
    )

def normalize_azure(raw: Any, input_text: str) -> SafetyResult:
    categories = {}
    for cat_res in raw.categories:
        sev_val = cat_res.severity.value / 6.0
        categories[cat_res.category.name] = sev_val
    flagged = any(sev_val > 0.5 for sev_val in categories.values())
    return SafetyResult(
        input_text=input_text,
        flagged=flagged,
        categories=categories
    )