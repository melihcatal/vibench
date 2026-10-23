"""
Moderate free-text claims or notes using OpenAI's Moderation API.
Checks user-submitted profile text for policy violations during federated login.
"""

import os
from typing import Optional, Dict, Any, List

from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODERATION_MODEL", "text-moderation-stable")


class ModerationError(Exception):
    """Raised when moderation check fails."""
    pass


def moderate_text(
    text: str,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate a single text string using OpenAI Moderation API.

    Returns moderation results including flagged categories and scores.
    Uses the text-moderation-stable model by default.
    """
    client = OpenAI(
        api_key=api_key or OPENAI_API_KEY,
    )

    try:
        response = client.moderations.create(
            model=model or OPENAI_MODEL,
            input=text,
        )
    except Exception as exc:
        raise ModerationError(f"OpenAI moderation failed: {exc}") from exc

    result = response.results[0]

    return {
        "flagged": result.flagged,
        "categories": dict(result.category_scores),
        "category_applied_input_types": dict(result.categories),
        "model": model or OPENAI_MODEL,
        "provider": "openai",
    }


def moderate_claims(
    claims: Dict[str, str],
    fields_to_check: Optional[List[str]] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate multiple claim fields from a federated user profile.

    Checks specified text fields against OpenAI's content policy.
    """
    check_fields = fields_to_check or [
        "name",
        "given_name",
        "family_name",
        "nickname",
        "bio",
        "notes",
    ]

    results = {}
    overall_flagged = False

    for field in check_fields:
        text = claims.get(field, "")
        if not text:
            continue

        moderation = moderate_text(text, api_key=api_key, model=model)
        results[field] = moderation

        if moderation["flagged"]:
            overall_flagged = True

    return {
        "results": results,
        "overall_flagged": overall_flagged,
        "fields_checked": list(results.keys()),
        "model": model or OPENAI_MODEL,
        "provider": "openai",
    }


def moderate_user_profile_notes(
    user_notes: str,
    additional_context: Optional[str] = None,
    api_key: Optional[str] = None,
    model: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate free-text notes associated with a user profile.

    Combines notes with optional context for more accurate moderation.
    """
    text_to_check = user_notes
    if additional_context:
        text_to_check = f"{additional_context}\n---\n{user_notes}"

    moderation = moderate_text(text_to_check, api_key=api_key, model=model)

    return {
        "notes_flagged": moderation["flagged"],
        "categories": moderation["categories"],
        "categories_applied": moderation["category_applied_input_types"],
        "model": model or OPENAI_MODEL,
        "provider": "openai",
    }


def build_moderation_decision(
    moderation_result: Dict[str, Any],
    auto_reject_categories: Optional[List[str]] = None,
) -> Dict[str, Any]:
    """
    Build an automated moderation decision based on OpenAI results.

    Auto-rejects if specific violation categories are triggered.
    """
    reject_categories = auto_reject_categories or [
        "hate",
        "hate/threatening",
        "self-harm",
        "sexual",
        "sexual/minors",
        "violence",
        "violence/graphic",
    ]

    flagged = moderation_result.get("flagged", False)
    categories = moderation_result.get("categories", {})

    triggered_rejections = [
        cat for cat in reject_categories
        if categories.get(cat, False)
    ]

    decision = "approved"
    if flagged and triggered_rejections:
        decision = "rejected"
    elif flagged:
        decision = "review"

    return {
        "decision": decision,
        "flagged": flagged,
        "triggered_rejections": triggered_rejections,
        "requires_manual_review": decision == "review",
        "moderation_model": moderation_result.get("model", OPENAI_MODEL),
        "provider": "openai",
    }


if __name__ == "__main__":
    sample_text = "This is a benign user bio for testing."
    result = moderate_text(sample_text)
    print(f"Flagged: {result['flagged']}")
    print(f"Provider: {result['provider']}")
    print(f"Model: {result['model']}")
