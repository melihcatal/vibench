"""
prompt_safety.py - Check prompts and generated text for unsafe content.

Uses OpenAI's Moderation API (api.openai.com) to screen text for safety violations.
"""

from typing import Union

from model_client import get_openai_client
from model_models import SafetyCheckResult


OPENAI_MODERATION_ENDPOINT = "https://api.openai.com/v1/moderations"

SAFETY_CATEGORIES = [
    "hate",
    "hate/threatening",
    "harassment",
    "harassment/threatening",
    "self-harm",
    "self-harm/intent",
    "self-harm/instructions",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


def check_prompt_safety(text: str) -> SafetyCheckResult:
    """
    Check if the provided text (prompt or generated content) is safe
    using OpenAI's Moderation API.

    Args:
        text: The text to evaluate for unsafe content.

    Returns:
        SafetyCheckResult with per-category flags and overall safety verdict.
    """
    client = get_openai_client()

    moderation = client.moderations.create(input=text)

    if not moderation.results:
        return SafetyCheckResult(
            is_safe=True,
            details="No moderation results returned.",
        )

    result = moderation.results[0]
    categories = {}
    flagged = []

    for cat in SAFETY_CATEGORIES:
        flag_value = getattr(result.flagged_categories, cat, False)
        categories[cat] = flag_value
        if flag_value:
            flagged.append(cat)

    is_safe = not result.flagged

    return SafetyCheckResult(
        is_safe=is_safe,
        categories=categories,
        flagged_categories=flagged,
        details=f"OpenAI moderation flagged={is_safe}",
    )


def check_safety_batch(texts: list[str]) -> list[SafetyCheckResult]:
    """
    Check multiple texts for safety in a single OpenAI moderation API call.

    Args:
        texts: List of texts to evaluate.

    Returns:
        List of SafetyCheckResult objects, one per input text.
    """
    client = get_openai_client()

    moderation = client.moderations.create(input=texts)

    results = []
    for mod_result in moderation.results:
        categories = {}
        flagged = []

        for cat in SAFETY_CATEGORIES:
            flag_value = getattr(mod_result.flagged_categories, cat, False)
            categories[cat] = flag_value
            if flag_value:
                flagged.append(cat)

        is_safe = not mod_result.flagged

        results.append(SafetyCheckResult(
            is_safe=is_safe,
            categories=categories,
            flagged_categories=flagged,
        ))

    return results


def is_text_safe(text: str, strict: bool = False) -> bool:
    """
    Quick boolean safety check using OpenAI moderation.

    Args:
        text: Text to check.
        strict: If True, also flag borderline high-score categories.

    Returns:
        True if text is safe, False otherwise.
    """
    client = get_openai_client()
    moderation = client.moderations.create(input=text)

    if not moderation.results:
        return True

    result = moderation.results[0]
    if result.flagged:
        return False

    if strict:
        for cat in SAFETY_CATEGORIES:
            score = getattr(result.category_scores, cat, 0.0)
            if score > 0.5:
                return False

    return True


def filter_safe_texts(texts: list[str]) -> list[str]:
    """
    Filter a list of texts, keeping only those that pass OpenAI moderation.

    Args:
        texts: List of texts to filter.

    Returns:
        List of texts that are marked as safe.
    """
    results = check_safety_batch(texts)
    return [text for text, result in zip(texts, results) if result.is_safe]


if __name__ == "__main__":
    test_prompts = [
        "Hello, how can I help you today?",
        "This is a very problematic and harmful request.",
        "Can you write a poem about the sunset?",
    ]

    for prompt in test_prompts:
        result = check_prompt_safety(prompt)
        print(f"Text: {prompt[:50]}... | Safe: {result.is_safe} | Flagged: {result.flagged_categories}")
