from __future__ import annotations

from typing import Optional

from model_client import get_platform_client, DEFAULT_MODERATION_MODEL
from model_models import SafetyResult


def check_platform_output_safety(
    text: str,
    model: str = DEFAULT_MODERATION_MODEL,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> SafetyResult:
    client = get_platform_client(
        api_key=api_key,
        organization=organization,
        project=project,
    )

    moderation_result = client.create_moderation(text=text, model=model)

    return SafetyResult(
        flagged=moderation_result["flagged"],
        categories=moderation_result["categories"],
        category_scores=moderation_result["category_scores"],
        raw_response=moderation_result["raw_response"],
    )


def is_content_safe(
    text: str,
    model: str = DEFAULT_MODERATION_MODEL,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> bool:
    result = check_platform_output_safety(
        text=text,
        model=model,
        api_key=api_key,
        organization=organization,
        project=project,
    )
    return not result.flagged


def get_safety_categories(
    text: str,
    model: str = DEFAULT_MODERATION_MODEL,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> dict:
    result = check_platform_output_safety(
        text=text,
        model=model,
        api_key=api_key,
        organization=organization,
        project=project,
    )
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "category_scores": result.category_scores,
    }


def check_multiple_texts(
    texts: list[str],
    model: str = DEFAULT_MODERATION_MODEL,
    api_key: Optional[str] = None,
    organization: Optional[str] = None,
    project: Optional[str] = None,
) -> list[SafetyResult]:
    results = []
    for text in texts:
        result = check_platform_output_safety(
            text=text,
            model=model,
            api_key=api_key,
            organization=organization,
            project=project,
        )
        results.append(result)
    return results
