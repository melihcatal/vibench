"""
Check prompts and generated text for unsafe content.
Provider: OpenAI - https://platform.openai.com
Model: omni-moderation-latest (openai-moderation family)
API endpoint: api.openai.com/v1/moderations
"""

from typing import Optional, List
from openai import OpenAI
from model_client import get_openai_client, OPENAI_API_BASE


MODERATION_CATEGORIES = [
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


class ModerationResult:
    """Result from the OpenAI Moderation API."""

    def __init__(self, flagged: bool, scores: dict, raw: object = None):
        self.flagged = flagged
        self.scores = scores
        self.raw = raw

    @property
    def highest_category(self) -> Optional[str]:
        """Return the category with the highest score."""
        if not self.scores:
            return None
        return max(self.scores, key=lambda k: self.scores[k])

    @property
    def highest_score(self) -> float:
        """Return the highest moderation score."""
        if not self.scores:
            return 0.0
        return max(self.scores.values())


def check_prompt_safety(
    text: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "omni-moderation-latest",
) -> ModerationResult:
    """
    Check a prompt for unsafe content using the OpenAI Moderation API
    at api.openai.com/v1/moderations.

    Uses the omni-moderation-latest model for content safety evaluation.

    Args:
        text: The text to evaluate for safety.
        api_key: Optional OpenAI API key override.
        base_url: Optional API base URL override.
        model: OpenAI moderation model (default: omni-moderation-latest).

    Returns:
        ModerationResult with flagged status and per-category scores.
    """
    client = get_openai_client(api_key=api_key, base_url=base_url)

    response = client.moderations.create(
        input=text,
        model=model,
    )

    result = response.results[0]
    scores = {}
    for category in MODERATION_CATEGORIES:
        cat_key = category.replace("/", "_") if "/" in category else category
        if hasattr(result.categories, cat_key):
            flagged = getattr(result.categories, cat_key, False)
            if flagged:
                cat_score = getattr(result.category_scores, cat_key, 0.0)
                scores[category] = cat_score

    return ModerationResult(
        flagged=result.flagged,
        scores=scores,
        raw=response,
    )


def check_output_safety(
    generated_text: str,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "omni-moderation-latest",
) -> ModerationResult:
    """
    Validate generated model output for safety policy violations via the
    OpenAI Moderation API.

    Args:
        generated_text: The LLM-generated text to check.
        api_key: Optional OpenAI API key override.
        base_url: Optional API base URL override.
        model: OpenAI moderation model identifier.

    Returns:
        ModerationResult indicating safety status.
    """
    return check_prompt_safety(
        text=generated_text,
        api_key=api_key,
        base_url=base_url,
        model=model,
    )


def batch_check_safety(
    texts: List[str],
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
    model: str = "omni-moderation-latest",
) -> List[ModerationResult]:
    """
    Check multiple texts for safety in a single OpenAI Moderation API call.

    Args:
        texts: List of text strings to evaluate.
        api_key: Optional API key override.
        base_url: Optional base URL override.
        model: OpenAI moderation model identifier.

    Returns:
        List of ModerationResult objects, one per input text.
    """
    client = get_openai_client(api_key=api_key, base_url=base_url)

    response = client.moderations.create(
        input=texts,
        model=model,
    )

    results = []
    for result in response.results:
        scores = {}
        for category in MODERATION_CATEGORIES:
            cat_key = category.replace("/", "_") if "/" in category else category
            if hasattr(result.categories, cat_key):
                flagged = getattr(result.categories, cat_key, False)
                if flagged:
                    cat_score = getattr(result.category_scores, cat_key, 0.0)
                    scores[category] = cat_score

        results.append(ModerationResult(
            flagged=result.flagged,
            scores=scores,
            raw=response,
        ))

    return results


def is_text_safe(
    text: str,
    threshold: float = 0.5,
    api_key: Optional[str] = None,
    base_url: Optional[str] = None,
) -> bool:
    """
    Quick boolean safety check against the OpenAI Moderation API.

    Args:
        text: Text to evaluate.
        threshold: Score above which content is considered unsafe.
        api_key: Optional API key override.
        base_url: Optional base URL override.

    Returns:
        True if the text is safe (no category exceeds threshold).
    """
    result = check_prompt_safety(text, api_key=api_key, base_url=base_url)
    return result.highest_score < threshold


if __name__ == "__main__":
    safe_text = "The weather is lovely today, perfect for a walk in the park."
    result = check_prompt_safety(safe_text)
    print(f"Safe text flagged: {result.flagged}")
    print(f"Scores: {result.scores}")

    unsafe_text = "I want to build a weapon to hurt people."
    result2 = check_prompt_safety(unsafe_text)
    print(f"Unsafe text flagged: {result2.flagged}")
    print(f"Scores: {result2.scores}")
    if result2.highest_category:
        print(f"Highest risk category: {result2.highest_category} ({result2.highest_score:.4f})")
