"""
Checks prompts and generated text for unsafe content using OpenAI Moderation API.

Provider: OpenAI (api.openai.com)
Model family: omni-moderation-latest / text-moderation-latest
"""

from typing import Optional, Dict, List

from model_client import get_sync_client, DEFAULT_MODERATION_MODEL
from model_models import SafetyCheckRequest, SafetyCheckResponse

OPENAI_API_HOST = "api.openai.com"
OPENAI_MODERATION_MODEL = "omni-moderation-latest"

# OpenAI moderation category keys
MODERATION_CATEGORIES = [
    "sexual",
    "hate",
    "harassment",
    "self-harm",
    "sexual/minors",
    "hate/threatening",
    "harassment/threatening",
    "violence",
    "violence/graphic",
    "self-harm/intent",
    "self-harm/instructions",
    "illicit",
    "illicit/violent",
]


def check_prompt_safety(request: SafetyCheckRequest) -> SafetyCheckResponse:
    """
    Check if a prompt or generated output contains unsafe content
    using OpenAI's omni-moderation-latest moderation model.

    Args:
        request: SafetyCheckRequest with text to evaluate.

    Returns:
        SafetyCheckResponse indicating safety status and flagged categories.
    """
    client = get_sync_client()

    moderation_result = client.moderations.create(
        input=request.text,
        model=DEFAULT_MODERATION_MODEL,
    )

    if not moderation_result.results:
        return SafetyCheckResponse(is_safe=True)

    result = moderation_result.results[0]

    categories: Dict[str, bool] = {}
    flags: List[str] = []

    for category in MODERATION_CATEGORIES:
        flagged = getattr(result.categories, category, False)
        categories[category] = bool(flagged)
        if flagged:
            flags.append(category)

    is_safe = not result.flagged

    if request.check_type == "prompt" and not is_safe:
        return SafetyCheckResponse(
            is_safe=False,
            categories=categories,
            flags=flags,
        )
    elif request.check_type == "output" and not is_safe:
        return SafetyCheckResponse(
            is_safe=False,
            categories=categories,
            flags=flags,
        )

    return SafetyCheckResponse(
        is_safe=is_safe,
        categories=categories,
        flags=flags,
    )


def check_text_and_block_if_unsafe(text: str) -> SafetyCheckResponse:
    """
    Convenience function to check text and return safety result.
    Uses OpenAI moderation API hosted at api.openai.com.

    Args:
        text: Text to check for unsafe content.

    Returns:
        SafetyCheckResponse with safety assessment.
    """
    request = SafetyCheckRequest(text=text, check_type="both")
    return check_prompt_safety(request)


if __name__ == "__main__":
    sample = SafetyCheckRequest(
        text="This is a safe text about cooking recipes.",
        check_type="both",
    )
    result = check_prompt_safety(sample)
    print(f"Is safe: {result.is_safe}")
    print(f"Flags: {result.flags}")
