"""
Moderate free-text claims or notes using OpenAI's content moderation API.

Validates user-submitted text fields (profile notes, bios, descriptions)
against OpenAI's moderation model to detect harmful, abusive, or
policy-violating content before storing it in user profiles.
"""

import os
from typing import Any, Dict, List, Optional

import openai
from openai import OpenAI


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = os.environ.get(
    "OPENAI_MODERATION_MODEL",
    "omni-moderation-latest",
)


class ModerationError(Exception):
    """Raised when content moderation fails or is blocked."""
    pass


def create_openai_client() -> OpenAI:
    """Create an OpenAI client configured with the API key."""
    return OpenAI(api_key=OPENAI_API_KEY)


def moderate_text(
    text: str,
    model: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Moderate free-text content using the OpenAI moderation API.

    Sends the text to OpenAI's moderation endpoint which returns
    category flags (hate, self-harm, sexual, violence, harassment,
    self-harm/intent, self-harm/instructions, sexual/minors,
    violence/graphic) and confidence scores.

    Uses the omni-moderation-latest model by default, which is
    OpenAI's latest moderation model supporting multimodal inputs.
    """
    if client is None:
        client = create_openai_client()

    mod_model = model or OPENAI_MODERATION_MODEL

    response = client.moderations.create(
        model=mod_model,
        input=text,
    )

    result = response.results[0]

    return {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "model_used": mod_model,
    }


def moderate_user_claim(
    claim_text: str,
    field_name: str = "note",
    strict: bool = False,
    model: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Any]:
    """
    Moderate a specific user claim or note field.

    Evaluates whether the text is safe to store in the federated user
    profile. When strict=True, rejects content with any elevated
    confidence score even if not strictly flagged.

    Args:
        claim_text: The free-text content to moderate.
        field_name: Name of the profile field being moderated.
        strict: If True, use lower thresholds for rejection.
        model: OpenAI moderation model to use.
        client: OpenAI client instance.

    Returns:
        Dict with moderation decision, details, and recommendation.
    """
    result = moderate_text(claim_text, model=model, client=client)

    threshold = 0.1 if strict else 0.3
    flagged_categories = [
        cat for cat, score in result["category_scores"].items()
        if score > threshold
    ]

    action = "approve"
    if result["flagged"] or (strict and flagged_categories):
        action = "reject"

    recommendation = _generate_recommendation(
        result, flagged_categories, field_name
    )

    return {
        "field": field_name,
        "text_length": len(claim_text),
        "flagged": result["flagged"],
        "action": action,
        "flagged_categories": flagged_categories,
        "category_scores": result["category_scores"],
        "recommendation": recommendation,
        "model_used": result["model_used"],
    }


def _generate_recommendation(
    result: Dict[str, Any],
    flagged_categories: List[str],
    field_name: str,
) -> str:
    """Generate a human-readable moderation recommendation."""
    if not result["flagged"] and not flagged_categories:
        return f"Content in '{field_name}' is safe to store."

    reasons = []
    for cat in flagged_categories:
        score = result["category_scores"].get(cat, 0)
        reasons.append(f"{cat} (score: {score:.4f})")

    return (
        f"Content in '{field_name}' requires review. "
        f"Flagged for: {', '.join(reasons)}"
    )


def moderate_multiple_claims(
    claims: Dict[str, str],
    strict: bool = False,
    model: Optional[str] = None,
    client: Optional[OpenAI] = None,
) -> Dict[str, Dict[str, Any]]:
    """
    Moderate multiple user claim fields at once.

    Checks each text field in the claims dict through OpenAI's
    moderation API and returns per-field results.
    """
    results = {}
    for field_name, text in claims.items():
        if not text or not text.strip():
            results[field_name] = {
                "field": field_name,
                "text_length": len(text) if text else 0,
                "flagged": False,
                "action": "approve",
                "flagged_categories": [],
                "category_scores": {},
                "recommendation": f"Empty field '{field_name}' - no moderation needed.",
                "model_used": model or OPENAI_MODERATION_MODEL,
            }
            continue

        results[field_name] = moderate_user_claim(
            claim_text=text,
            field_name=field_name,
            strict=strict,
            model=model,
            client=client,
        )

    return results


def get_moderation_summary(
    results: Dict[str, Dict[str, Any]],
) -> Dict[str, Any]:
    """
    Summarize moderation results across all fields.

    Returns an overall pass/fail status and lists which fields
    were flagged.
    """
    flagged_fields = [
        field for field, result in results.items()
        if result.get("flagged") or result.get("action") == "reject"
    ]

    total = len(results)
    approved = total - len(flagged_fields)

    return {
        "total_fields_moderated": total,
        "approved": approved,
        "flagged": len(flagged_fields),
        "flagged_fields": flagged_fields,
        "overall_status": "pass" if not flagged_fields else "review_required",
        "model_used": OPENAI_MODERATION_MODEL,
    }


if __name__ == "__main__":
    print("OpenAI claims moderation handler ready.")
    print(f"Model: {OPENAI_MODERATION_MODEL}")
