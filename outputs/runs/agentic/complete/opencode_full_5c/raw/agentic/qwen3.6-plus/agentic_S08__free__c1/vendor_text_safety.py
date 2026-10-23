import os

from openai import OpenAI

from document_models import ModerationResult


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "omni-moderation-latest")


def moderate_vendor_text(text: str) -> ModerationResult:
    if not text or not text.strip():
        return ModerationResult(
            is_safe=True,
            categories={},
            category_scores={},
            flagged_reasons=[],
        )

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )

    result = response.results[0]
    flagged = result.flagged
    categories = {}
    category_scores = {}
    flagged_reasons = []

    for cat_name, is_flagged in result.categories.model_dump().items():
        categories[cat_name] = is_flagged
        if is_flagged:
            flagged_reasons.append(cat_name)

    if hasattr(result, "category_scores"):
        scores_data = result.category_scores.model_dump()
        for cat_name, score in scores_data.items():
            category_scores[cat_name] = score

    return ModerationResult(
        is_safe=not flagged,
        categories=categories,
        category_scores=category_scores,
        flagged_reasons=flagged_reasons,
    )
