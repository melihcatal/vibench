import os
from typing import Dict, Any
from safety_client import get_openai_client
from safety_models import ModerationCategory, ModerationResult

def apply_safety_thresholds(text: str, thresholds: Dict[str, float]) -> ModerationResult:
    client = get_openai_client()
    
    response = client.moderations.create(input=text)
    moderation_output = response.results[0]

    categories = []
    overall_decision = "Safe"

    for category_name, flagged_status in moderation_output.categories.model_dump().items():
        if category_name in moderation_output.category_scores.model_dump():
            score = moderation_output.category_scores.model_dump()[category_name]
            is_violating = flagged_status or (score > thresholds.get(category_name, 0.0))
            
            severity = int(score * 100)
            
            categories.append(ModerationCategory(category=category_name, severity=severity, violates=is_violating))
            if is_violating:
                overall_decision = "Unsafe"
        else:
            if flagged_status:
                categories.append(ModerationCategory(category=category_name, severity=1, violates=True))
                overall_decision = "Unsafe"
    
    return ModerationResult(
        text=text,
        categories=categories,
        overall_decision=overall_decision,
        redacted_text=None,
        raw_response=moderation_output.model_dump()
    )
