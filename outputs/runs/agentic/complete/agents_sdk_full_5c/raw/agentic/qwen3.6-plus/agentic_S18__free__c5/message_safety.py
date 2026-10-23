"""Check message payload text for unsafe content using OpenAI Moderation API.

Uses the openai SDK with the text-moderation-latest moderation model to screen
message payloads for policy violations before processing or forwarding.
"""

import os
from dataclasses import dataclass
from typing import Any

import openai


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODERATION_MODEL = "text-moderation-latest"


@dataclass
class SafetyCheckResult:
    """Result of a content safety check on message payload text.

    Attributes:
        is_safe: Whether the content passed the safety check.
        categories: Dictionary of violation categories and their boolean flags.
        category_scores: Dictionary of violation category confidence scores.
        flagged_categories: List of categories that were flagged as violations.
    """
    is_safe: bool
    categories: dict[str, bool]
    category_scores: dict[str, float]
    flagged_categories: list[str]

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary representation.

        Returns:
            Dictionary with all safety check result fields.
        """
        return {
            "is_safe": self.is_safe,
            "categories": self.categories,
            "category_scores": self.category_scores,
            "flagged_categories": self.flagged_categories,
        }


def _get_openai_client() -> openai.OpenAI:
    """Create and return an OpenAI API client for moderation checks.

    Returns:
        Configured openai.OpenAI client instance.
    """
    return openai.OpenAI(api_key=OPENAI_API_KEY)


def check_message_safety(
    text: str,
    model: str = OPENAI_MODERATION_MODEL,
) -> SafetyCheckResult:
    """Check message payload text for unsafe content using OpenAI moderation.

    Uses the text-moderation-latest model to analyze text for policy violations
    including hate speech, self-harm, sexual content, and violence.

    Args:
        text: The message payload text to analyze.
        model: OpenAI moderation model ID. Defaults to text-moderation-latest.

    Returns:
        SafetyCheckResult with safety assessment details.

    Raises:
        openai.APIError: If the OpenAI moderation API call fails.
    """
    client = _get_openai_client()

    response = client.moderations.create(
        model=model,
        input=text,
    )

    result = response.results[0]
    flagged = result.flagged

    categories = {}
    category_scores = {}
    flagged_categories = []

    for category, is_flagged in result.categories.model_dump().items():
        categories[category] = is_flagged
        if is_flagged:
            flagged_categories.append(category)

    for category, score in result.category_scores.model_dump().items():
        category_scores[category] = score

    return SafetyCheckResult(
        is_safe=not flagged,
        categories=categories,
        category_scores=category_scores,
        flagged_categories=flagged_categories,
    )


def check_payload_safety(
    payload: dict[str, Any],
    text_fields: list[str] | None = None,
) -> SafetyCheckResult | None:
    """Check specific text fields within a message payload for unsafe content.

    Extracts text from specified fields in the payload dictionary and runs
    safety checks on each. Returns a combined safety result.

    Args:
        payload: The message payload dictionary to check.
        text_fields: List of field names to check. Defaults to common text fields.

    Returns:
        SafetyCheckResult if text was found, None if no text fields present.
    """
    if text_fields is None:
        text_fields = ["text", "message", "content", "description", "body", "comment"]

    all_text = []
    for field_name in text_fields:
        value = payload.get(field_name)
        if value and isinstance(value, str):
            all_text.append(value)

    if not all_text:
        return None

    combined_text = " ".join(all_text)
    return check_message_safety(combined_text)


def is_payload_safe(
    payload: dict[str, Any],
    text_fields: list[str] | None = None,
) -> bool:
    """Quick safety check returning only a boolean result.

    Args:
        payload: The message payload dictionary to check.
        text_fields: List of field names to check.

    Returns:
        True if the payload text is safe, False otherwise.
    """
    result = check_payload_safety(payload, text_fields)
    if result is None:
        return True
    return result.is_safe


if __name__ == "__main__":
    test_text = "This is a normal message with no issues."
    result = check_message_safety(test_text)
    print(f"Safe: {result.is_safe}")
    print(f"Flagged: {result.flagged_categories}")
