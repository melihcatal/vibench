import os

from openai import OpenAI
from vision_models import TextSafetyResult


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_BASE_URL = os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1")
OPENAI_MODERATION_MODEL = os.environ.get(
    "OPENAI_MODERATION_MODEL", "omni-moderation-latest"
)


def get_openai_client() -> OpenAI:
    return OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_BASE_URL,
    )


def check_visual_safety_text(text: str) -> TextSafetyResult:
    client = get_openai_client()
    response = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    result = response.results[0]
    flagged = result.flagged
    categories = {}
    flagged_terms = []

    for category_name, is_flagged in result.categories.model_dump().items():
        score = result.category_scores.model_dump().get(category_name, 0.0)
        categories[category_name] = {
            "flagged": is_flagged,
            "score": round(score, 4),
        }
        if is_flagged:
            flagged_terms.append(category_name)

    overall_confidence = max(
        (result.category_scores.model_dump().get(cat, 0.0) for cat in flagged_terms),
        default=0.0,
    )

    return TextSafetyResult(
        is_safe=not flagged,
        flagged_terms=flagged_terms,
        categories=categories,
        confidence=round(overall_confidence, 4),
    )


def check_labels_safety_text(labels_text: str) -> TextSafetyResult:
    return check_visual_safety_text(labels_text)


def check_batch_safety_text(texts: list[str]) -> list[TextSafetyResult]:
    results = []
    for text in texts:
        result = check_visual_safety_text(text)
        results.append(result)
    return results
