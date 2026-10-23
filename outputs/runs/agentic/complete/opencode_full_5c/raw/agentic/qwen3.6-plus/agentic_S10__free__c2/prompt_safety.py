from __future__ import annotations

from typing import Optional

from model_client import create_moderation
from model_models import SafetyResponse, normalize_prompt

MODERATION_MODEL = "omni-moderation-latest"


def check_prompt_safety(
    text: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> SafetyResponse:
    normalized = normalize_prompt(text)
    result = create_moderation(normalized, api_key=api_key, base_url=base_url)
    flagged_categories = [
        cat for cat, flagged in result["categories"].items() if flagged
    ]
    return SafetyResponse(
        is_safe=not result["flagged"],
        categories=result["categories"],
        category_scores=result["category_scores"],
        flagged_categories=flagged_categories,
        raw=result,
    )


def check_output_safety(
    generated_text: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> SafetyResponse:
    normalized = normalize_prompt(generated_text)
    result = create_moderation(normalized, api_key=api_key, base_url=base_url)
    flagged_categories = [
        cat for cat, flagged in result["categories"].items() if flagged
    ]
    return SafetyResponse(
        is_safe=not result["flagged"],
        categories=result["categories"],
        category_scores=result["category_scores"],
        flagged_categories=flagged_categories,
        raw=result,
    )


def is_content_safe(
    text: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> bool:
    response = check_prompt_safety(text, api_key=api_key, base_url=base_url)
    return response.is_safe


def get_safety_report(
    text: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> dict:
    response = check_prompt_safety(text, api_key=api_key, base_url=base_url)
    return {
        "is_safe": response.is_safe,
        "flagged_categories": response.flagged_categories,
        "category_scores": {
            k: round(v, 4) for k, v in response.category_scores.items()
        },
    }


if __name__ == "__main__":
    import os

    report = get_safety_report(
        text="This is a perfectly safe and benign text about weather.",
        api_key=os.environ.get("OPENAI_API_KEY"),
    )
    print(report)
