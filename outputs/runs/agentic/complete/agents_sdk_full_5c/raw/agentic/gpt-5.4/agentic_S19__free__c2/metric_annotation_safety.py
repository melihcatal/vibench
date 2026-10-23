from __future__ import annotations

from openai import OpenAI

from observability_models import SafetyAssessment


OPENAI_MODEL = "omni-moderation-latest"


def metric_annotation_safety(text: str) -> SafetyAssessment:
    client = OpenAI()
    response = client.moderations.create(model=OPENAI_MODEL, input=text)
    result = response.results[0]
    flagged_map = result.categories.model_dump()
    flagged_categories = [name for name, flagged in flagged_map.items() if flagged]
    scores = result.category_scores.model_dump()
    top_category = max(scores, key=scores.get)
    return SafetyAssessment(
        text=text,
        safe=not result.flagged,
        category=flagged_categories[0] if flagged_categories else top_category,
        confidence=float(scores.get(top_category, 0.0)),
        provider="api.openai.com",
    )
