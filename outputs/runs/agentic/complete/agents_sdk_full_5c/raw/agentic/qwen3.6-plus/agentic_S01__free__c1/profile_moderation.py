"""
Moderate profile text before account activation using OpenAI Moderation API.
Provider: OpenAI Moderation API (openai package)
"""

import os
from typing import Dict, Any, Optional, List

import openai


OPENAI_MODERATION_MODEL_ID = "text-moderation-latest"


def moderate_profile_text(
    display_name: str = "",
    bio: str = "",
    profile_text: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Moderate profile text content using OpenAI's Moderation API.

    Checks for violations including:
    - Hate speech
    - Self-harm content
    - Sexual content
    - Violence
    - Harassment

    Args:
        display_name: User display name
        bio: User bio/about text
        profile_text: Additional profile text to moderate
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var)

    Returns:
        Dict with moderation results including flags and verdict
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return _error_result("OpenAI API key not configured")

    text_to_moderate = _combine_profile_text(display_name, bio, profile_text)
    if not text_to_moderate.strip():
        return _empty_result()

    client = openai.OpenAI(api_key=key)

    try:
        response = client.moderations.create(
            model=OPENAI_MODERATION_MODEL_ID,
            input=text_to_moderate,
        )

        result = response.results[0]

        categories = {}
        category_scores = {}
        if hasattr(result, "categories"):
            categories = dict(result.categories)
        if hasattr(result, "category_scores"):
            category_scores = {k: float(v) for k, v in dict(result.category_scores).items()}

        flagged = bool(result.flagged)

        verdict = "approved" if not flagged else "flagged"
        if _has_high_risk_categories(categories):
            verdict = "blocked"

        return {
            "verdict": verdict,
            "flagged": flagged,
            "categories": categories,
            "category_scores": category_scores,
            "model": OPENAI_MODERATION_MODEL_ID,
            "provider": "openai_moderation",
            "text_length": len(text_to_moderate),
            "success": True,
        }

    except openai.APIError as exc:
        return _error_result(f"OpenAI API error: {str(exc)}")
    except openai.RateLimitError:
        return _error_result("OpenAI rate limit exceeded")
    except openai.AuthenticationError:
        return _error_result("OpenAI authentication failed")
    except Exception as exc:
        return _error_result(f"Unexpected error: {str(exc)}")


def moderate_batch(
    profiles: List[Dict[str, str]],
    api_key: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """
    Moderate multiple profiles in batch.

    Args:
        profiles: List of dicts with display_name, bio, profile_text keys
        api_key: OpenAI API key

    Returns:
        List of moderation results
    """
    results = []
    for profile in profiles:
        result = moderate_profile_text(
            display_name=profile.get("display_name", ""),
            bio=profile.get("bio", ""),
            profile_text=profile.get("profile_text"),
            api_key=api_key,
        )
        result["profile_id"] = profile.get("profile_id")
        results.append(result)
    return results


def is_profile_safe(moderation_result: Dict[str, Any]) -> bool:
    """
    Check if a moderation result indicates the profile is safe.

    Args:
        moderation_result: Result from moderate_profile_text

    Returns:
        True if profile is approved
    """
    return moderation_result.get("verdict") == "approved"


def get_flagged_categories(moderation_result: Dict[str, Any]) -> List[str]:
    """
    Get list of categories that were flagged in moderation.

    Args:
        moderation_result: Result from moderate_profile_text

    Returns:
        List of flagged category names
    """
    categories = moderation_result.get("categories", {})
    return [cat for cat, flagged in categories.items() if flagged]


def _combine_profile_text(
    display_name: str,
    bio: str,
    profile_text: Optional[str],
) -> str:
    """Combine profile fields into single text for moderation."""
    parts = []
    if display_name:
        parts.append(f"Name: {display_name}")
    if bio:
        parts.append(f"Bio: {bio}")
    if profile_text:
        parts.append(f"Profile: {profile_text}")
    return " | ".join(parts)


def _has_high_risk_categories(categories: Dict[str, bool]) -> bool:
    """Check if any high-risk categories are flagged."""
    high_risk = ["hate", "self-harm", "sexual/minors", "violence"]
    return any(categories.get(cat, False) for cat in high_risk)


def _error_result(error_message: str) -> Dict[str, Any]:
    """Return an error moderation result."""
    return {
        "verdict": "error",
        "flagged": False,
        "categories": {},
        "category_scores": {},
        "model": OPENAI_MODERATION_MODEL_ID,
        "provider": "openai_moderation",
        "text_length": 0,
        "success": False,
        "error": error_message,
    }


def _empty_result() -> Dict[str, Any]:
    """Return an empty text moderation result."""
    return {
        "verdict": "approved",
        "flagged": False,
        "categories": {},
        "category_scores": {},
        "model": OPENAI_MODERATION_MODEL_ID,
        "provider": "openai_moderation",
        "text_length": 0,
        "success": True,
    }


if __name__ == "__main__":
    import sys

    display_name = sys.argv[1] if len(sys.argv) > 1 else "TestUser"
    bio = sys.argv[2] if len(sys.argv) > 2 else "Hello, I am new here!"

    result = moderate_profile_text(display_name=display_name, bio=bio)
    print(f"Moderation verdict: {result['verdict']}")
    if result.get("flagged"):
        print(f"Flagged categories: {get_flagged_categories(result)}")
