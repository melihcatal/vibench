"""
prompt_safety.py — Check prompts and generated text for unsafe content.

Uses the OpenAI Moderations API (api.openai.com) to evaluate text against
content-safety categories. Compatible with the OpenAI moderation model
omni-moderation-2024-09-26 (via the openai SDK moderation endpoint).
"""

from __future__ import annotations

from typing import Optional

from model_client import check_moderation, get_openai_client
from model_models import ModerationRequest, ModerationResponse

# The OpenAI moderation endpoint uses the hosted moderation model
# managed by OpenAI at api.openai.com.
MODERATION_ENDPOINT = "https://api.openai.com/v1/moderations"


def check_prompt_safety(
    text: str,
    fail_on_flagged: bool = True,
) -> ModerationResponse:
    """
    Check a prompt for unsafe content using the OpenAI Moderations API.

    Parameters
    ----------
    text : str
        The text to evaluate.
    fail_on_flagged : bool
        If True, raise a ValueError when the text is flagged.

    Returns
    -------
    ModerationResponse
        Safety assessment with category flags and scores.

    Raises
    ------
    ValueError
        If the text is flagged and fail_on_flagged is True.
    """
    request = ModerationRequest(input_text=text)
    result = check_moderation(request)

    if fail_on_flagged and result.flagged:
        flagged_categories = [
            cat for cat, is_flagged in result.categories.items() if is_flagged
        ]
        raise ValueError(
            f"Content flagged as unsafe by OpenAI Moderations API "
            f"({MODERATION_ENDPOINT}). Categories: {flagged_categories}"
        )

    return result


def check_generated_text_safety(
    generated_text: str,
) -> ModerationResponse:
    """
    Validate model-generated output for unsafe content.

    Parameters
    ----------
    generated_text : str
        The text produced by an LLM to evaluate.

    Returns
    -------
    ModerationResponse
        Safety assessment with category flags and scores.
    """
    return check_prompt_safety(generated_text, fail_on_flagged=False)


def is_safe(
    text: str,
) -> bool:
    """
    Return True if the text passes OpenAI moderation checks.

    Parameters
    ----------
    text : str
        The text to evaluate.

    Returns
    -------
    bool
        True when no safety categories are triggered.
    """
    result = check_prompt_safety(text, fail_on_flagged=False)
    return not result.flagged


def get_safety_report(
    text: str,
) -> dict:
    """
    Return a detailed safety report with flagged categories and scores.

    Parameters
    ----------
    text : str
        The text to evaluate.

    Returns
    -------
    dict
        Report containing flagged status, category flags, and scores.
    """
    result = check_prompt_safety(text, fail_on_flagged=False)
    return {
        "flagged": result.flagged,
        "categories": result.categories,
        "scores": result.category_scores,
        "endpoint": MODERATION_ENDPOINT,
    }


if __name__ == "__main__":
    safe_text = "The quick brown fox jumps over the lazy dog."
    report = get_safety_report(safe_text)
    print(f"Safe text report: flagged={report['flagged']}")

    # Example with potentially flagged content (do not use in production)
    # unsafe_report = get_safety_report("This contains violence and hate speech.")
