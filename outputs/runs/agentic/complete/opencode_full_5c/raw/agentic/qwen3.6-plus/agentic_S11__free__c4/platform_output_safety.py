from __future__ import annotations

from typing import Optional

from openai import OpenAI

from model_client import PlatformClientConfig, create_openai_client
from model_models import SafetyResult


def check_platform_output_safety(
    text: str,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
) -> SafetyResult:
    openai_client = client or create_openai_client(config)

    result = openai_client.moderations.create(
        model="omni-moderation-latest",
        input=text,
    )

    mod_result = result.results[0]

    categories = {}
    category_scores = {}

    if hasattr(mod_result, "categories"):
        if isinstance(mod_result.categories, dict):
            categories = dict(mod_result.categories)
        else:
            cat_obj = mod_result.categories
            for attr in dir(cat_obj):
                if not attr.startswith("_") and not callable(getattr(cat_obj, attr)):
                    val = getattr(cat_obj, attr)
                    if isinstance(val, bool):
                        categories[attr] = val

    if hasattr(mod_result, "category_scores"):
        if isinstance(mod_result.category_scores, dict):
            category_scores = dict(mod_result.category_scores)
        else:
            scores_obj = mod_result.category_scores
            for attr in dir(scores_obj):
                if not attr.startswith("_") and not callable(getattr(scores_obj, attr)):
                    val = getattr(scores_obj, attr)
                    if isinstance(val, (int, float)):
                        category_scores[attr] = float(val)

    flagged = mod_result.flagged

    return SafetyResult(
        flagged=flagged,
        categories=categories,
        category_scores=category_scores,
        raw=result,
    )


def is_output_safe(
    text: str,
    client: Optional[OpenAI] = None,
    config: Optional[PlatformClientConfig] = None,
    strict: bool = False,
) -> bool:
    result = check_platform_output_safety(text, client=client, config=config)
    if strict:
        max_score = (
            max(result.category_scores.values()) if result.category_scores else 0.0
        )
        return not result.flagged and max_score < 0.3
    return not result.flagged


if __name__ == "__main__":
    safety = check_platform_output_safety("Hello, how are you today?")
    print(f"Flagged: {safety.flagged}")
    print(f"Categories: {safety.categories}")
