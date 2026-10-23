import os
from typing import Optional, Dict, Any, List

from openai import OpenAI


OPENAI_API_KEY_ENV = "OPENAI_API_KEY"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"

PROFILE_TEXT_FIELDS = ["display_name", "bio", "location", "website_description"]


def get_client() -> OpenAI:
    api_key = os.environ.get(OPENAI_API_KEY_ENV)
    return OpenAI(api_key=api_key)


def moderate_profile_text(
    text: str,
    field_name: Optional[str] = None,
) -> Dict[str, Any]:
    client = get_client()

    result = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    moderation_result = result.results[0]

    return {
        "field_name": field_name or "unknown",
        "text": text,
        "flagged": moderation_result.flagged,
        "categories": dict(moderation_result.categories),
        "category_scores": {
            k: round(v, 4) for k, v in dict(moderation_result.category_scores).items()
        },
        "approved": not moderation_result.flagged,
    }


def moderate_full_profile(
    profile_data: Dict[str, Any],
) -> Dict[str, Any]:
    client = get_client()
    results = []
    overall_approved = True

    for field in PROFILE_TEXT_FIELDS:
        text = profile_data.get(field)
        if not text or not isinstance(text, str):
            continue

        moderation_result = client.moderations.create(
            model=OPENAI_MODERATION_MODEL,
            input=text,
        )

        mod = moderation_result.results[0]
        field_result = {
            "field_name": field,
            "text": text,
            "flagged": mod.flagged,
            "categories": dict(mod.categories),
        }

        results.append(field_result)

        if mod.flagged:
            overall_approved = False

    return {
        "profile_moderated": True,
        "overall_approved": overall_approved,
        "field_results": results,
        "model_used": OPENAI_MODERATION_MODEL,
    }


def check_text_safe_for_onboarding(
    text: str,
    strict_mode: bool = True,
) -> bool:
    client = get_client()

    result = client.moderations.create(
        model=OPENAI_MODERATION_MODEL,
        input=text,
    )

    mod = result.results[0]

    if strict_mode:
        return not mod.flagged

    high_risk_categories = ["sexual/minors", "self-harm", "violence/graphic"]
    for category in high_risk_categories:
        if getattr(mod.categories, category.replace("/", "_").replace("-", "_"), False):
            return False

    return True
