"""
Check prompts and generated text for unsafe content using OpenAI Moderation API.

Uses OpenAI platform API at api.openai.com with concrete model text-moderation-latest
for content safety screening.
"""

import os
from typing import Any, Dict, List, Optional, Tuple

from openai import OpenAI


_OPENAI_MODERATION_MODEL = "text-moderation-latest"


def get_moderation_client() -> OpenAI:
    """Create OpenAI client for moderation API access."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=api_key, base_url="https://api.openai.com/v1")


def check_safety(
    text: str,
    model: str = _OPENAI_MODERATION_MODEL,
) -> Dict[str, Any]:
    """Check text for unsafe content using OpenAI's moderation model.

    Args:
        text: The text to screen for safety violations.
        model: OpenAI moderation model identifier (text-moderation-latest).

    Returns:
        Dict with 'flagged' boolean and 'categories' detail dict.
    """
    client = get_moderation_client()

    response = client.moderations.create(
        input=text,
        model=model,
    )

    result = response.results[0]
    return {
        "flagged": result.flagged,
        "categories": {
            "sexual": result.categories.sexual,
            "hate": result.categories.hate,
            "harassment": result.categories.harassment,
            "self-harm": result.categories.self_harm,
            "sexual/minors": result.categories.sexual_minors,
            "hate/threatening": result.categories.hate_threatening,
            "violence/graphic": result.categories.violence_graphic,
            "self-harm/intent": result.categories.self_harm_intent,
            "self-harm/instructions": result.categories.self_harm_instructions,
            "harassment/threatening": result.categories.harassment_threatening,
            "violence": result.categories.violence,
        },
        "category_scores": {
            cat: getattr(result.category_scores, cat, 0.0)
            for cat in dir(result.category_scores)
            if not cat.startswith("_") and not cat.startswith("get")
        },
    }


def check_prompt_safety(prompt: str) -> Tuple[bool, Optional[str]]:
    """Validate a prompt is safe before sending to the LLM.

    Args:
        prompt: The user prompt to screen.

    Returns:
        Tuple of (is_safe, reason_if_flagged).
    """
    result = check_safety(prompt)
    if result["flagged"]:
        flagged_cats = [
            cat for cat, is_flagged in result["categories"].items() if is_flagged
        ]
        return False, f"Prompt flagged for: {', '.join(flagged_cats)}"
    return True, None


def check_output_safety(generated_text: str) -> Tuple[bool, Optional[str]]:
    """Validate generated model output for safety compliance.

    Args:
        generated_text: The model's generated text to screen.

    Returns:
        Tuple of (is_safe, reason_if_flagged).
    """
    result = check_safety(generated_text)
    if result["flagged"]:
        flagged_cats = [
            cat for cat, is_flagged in result["categories"].items() if is_flagged
        ]
        return False, f"Output flagged for: {', '.join(flagged_cats)}"
    return True, None


def batch_check_safety(
    texts: List[str],
    model: str = _OPENAI_MODERATION_MODEL,
) -> List[Dict[str, Any]]:
    """Batch check multiple texts for safety using OpenAI moderation.

    Args:
        texts: List of texts to screen.
        model: OpenAI moderation model identifier.

    Returns:
        List of safety result dicts for each input text.
    """
    client = get_moderation_client()

    response = client.moderations.create(
        input=texts,
        model=model,
    )

    results = []
    for result in response.results:
        results.append({
            "flagged": result.flagged,
            "categories": {
                "sexual": result.categories.sexual,
                "hate": result.categories.hate,
                "harassment": result.categories.harassment,
                "self-harm": result.categories.self_harm,
                "violence": result.categories.violence,
                "sexual/minors": result.categories.sexual_minors,
            },
        })

    return results


def is_safe_for_use(text: str) -> bool:
    """Quick boolean check if text is safe.

    Args:
        text: Text to check.

    Returns:
        True if the text passes moderation, False otherwise.
    """
    result = check_safety(text)
    return not result["flagged"]


if __name__ == "__main__":
    test_text = "This is a perfectly safe test message about programming."
    result = check_safety(test_text)
    print(f"Flagged: {result['flagged']}")
    print(f"Categories: {result['categories']}")
