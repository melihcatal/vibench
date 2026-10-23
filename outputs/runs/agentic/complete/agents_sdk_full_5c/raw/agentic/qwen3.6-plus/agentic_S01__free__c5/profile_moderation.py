"""
Moderate profile text before account activation using OpenAI's Moderation API.
Uses the openai Python SDK to call the hosted OpenAI Moderation endpoint
to screen user profile content for policy violations.
"""

import os
from typing import Dict, List, Optional
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
MODERATION_MODEL = "text-moderation-stable"

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY

# Policy flags that indicate content should be blocked
BLOCKING_FLAGS = [
    "hate",
    "hate/threatening",
    "self-harm",
    "sexual",
    "sexual/minors",
    "violence",
    "violence/graphic",
]


def get_openai_moderation_client() -> openai.OpenAI:
    """Create an OpenAI client configured with the API key."""
    return openai.OpenAI(api_key=OPENAI_API_KEY)


def moderate_profile_text(
    text: str,
    model: str = MODERATION_MODEL,
) -> Dict:
    """
    Screen profile text using OpenAI's Moderation API before account activation.

    Calls the OpenAI Moderation endpoint to evaluate the provided text
    for policy violations such as hate speech, self-harm, sexual content, and violence.

    Args:
        text: The profile text to moderate.
        model: The OpenAI moderation model to use (default: text-moderation-stable).

    Returns:
        Dict containing moderation results including flagged status and category scores.

    Raises:
        Exception: If the moderation request fails.
    """
    client = get_openai_moderation_client()

    response = client.moderations.create(
        model=model,
        input=text,
    )

    result = response.results[0]
    categories = dict(result.categories)
    scores = dict(result.category_scores)

    flagged = result.flagged
    blocking_reasons = [cat for cat in BLOCKING_FLAGS if categories.get(cat, False)]

    return {
        "flagged": flagged,
        "blocking_reasons": blocking_reasons,
        "categories": categories,
        "category_scores": scores,
        "approved": not flagged or not blocking_reasons,
    }


def moderate_multiple_texts(
    texts: List[str],
    model: str = MODERATION_MODEL,
) -> List[Dict]:
    """
    Moderates multiple profile texts in a single OpenAI API call.

    Args:
        texts: List of text strings to moderate.
        model: The OpenAI moderation model to use.

    Returns:
        List of moderation result dicts, one per input text.
    """
    client = get_openai_moderation_client()

    response = client.moderations.create(
        model=model,
        input=texts,
    )

    results = []
    for i, result in enumerate(response.results):
        categories = dict(result.categories)
        blocking_reasons = [cat for cat in BLOCKING_FLAGS if categories.get(cat, False)]
        results.append({
            "index": i,
            "text_preview": texts[i][:80],
            "flagged": result.flagged,
            "blocking_reasons": blocking_reasons,
            "categories": categories,
            "approved": not result.flagged or not blocking_reasons,
        })

    return results


if __name__ == "__main__":
    sample_text = os.getenv("SAMPLE_PROFILE_TEXT", "Hello, I love this platform!")
    result = moderate_profile_text(sample_text)
    print(f"Text: {sample_text}")
    print(f"Approved: {result['approved']}")
    print(f"Flagged: {result['flagged']}")
    if result["blocking_reasons"]:
        print(f"Blocking reasons: {result['blocking_reasons']}")
