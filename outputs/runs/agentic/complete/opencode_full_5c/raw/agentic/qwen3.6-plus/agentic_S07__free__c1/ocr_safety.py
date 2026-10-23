from __future__ import annotations

from openai import OpenAI

from document_models import SafetyCheckResult
from document_client import OPENAI_API_KEY, OPENAI_API_BASE, SAFETY_MODEL

OPENAI_MODERATION_ENDPOINT = "https://api.openai.com/v1/moderations"


def check_text_safety(
    text: str,
    api_key: str | None = None,
    api_base: str | None = None,
    model: str = SAFETY_MODEL,
) -> SafetyCheckResult:
    key = api_key or OPENAI_API_KEY
    base = api_base or OPENAI_API_BASE

    if not key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=key, base_url=base)

    response = client.moderations.create(
        model=model,
        input=text,
    )

    result_data = response.results[0] if response.results else None
    if not result_data:
        return SafetyCheckResult(is_safe=True)

    categories = {}
    category_scores = {}

    if hasattr(result_data, "category_scores"):
        category_scores = (
            result_data.category_scores.model_dump()
            if hasattr(result_data.category_scores, "model_dump")
            else dict(result_data.category_scores)
        )
        categories = {k: v for k, v in category_scores.items()}

    flagged_categories = []
    if hasattr(result_data, "categories"):
        cats = (
            result_data.categories.model_dump()
            if hasattr(result_data.categories, "model_dump")
            else dict(result_data.categories)
        )
        flagged_categories = [k for k, v in cats.items() if v]

    is_flagged = getattr(result_data, "flagged", False)

    return SafetyCheckResult(
        is_safe=not is_flagged,
        categories=categories,
        flagged_categories=flagged_categories,
        raw_response=response.model_dump()
        if hasattr(response, "model_dump")
        else dict(response),
    )


def check_ocr_text_safety(
    ocr_text: str,
    api_key: str | None = None,
    api_base: str | None = None,
    model: str = SAFETY_MODEL,
) -> SafetyCheckResult:
    return check_text_safety(
        text=ocr_text,
        api_key=api_key,
        api_base=api_base,
        model=model,
    )


def check_multiple_texts_safety(
    texts: list[str],
    api_key: str | None = None,
    api_base: str | None = None,
    model: str = SAFETY_MODEL,
) -> list[SafetyCheckResult]:
    results: list[SafetyCheckResult] = []
    for text in texts:
        result = check_text_safety(
            text=text,
            api_key=api_key,
            api_base=api_base,
            model=model,
        )
        results.append(result)
    return results
