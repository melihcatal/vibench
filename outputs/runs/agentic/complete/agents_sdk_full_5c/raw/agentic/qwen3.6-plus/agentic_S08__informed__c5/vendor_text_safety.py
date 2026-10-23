"""
Moderate vendor notes or memo fields using Anthropic Messages API.

Provider: Anthropic Messages API (anthropic SDK)
Auth: ANTHROPIC_API_KEY environment variable
Model: claude-3-5-sonnet-20241022
"""

import json
import os
from typing import Dict, Any, Optional, List

import anthropic


ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def get_anthropic_client() -> anthropic.Anthropic:
    """
    Initialize and return an Anthropic API client.

    Requires ANTHROPIC_API_KEY environment variable.

    Returns:
        anthropic.Anthropic client instance.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic Messages API."
        )
    return anthropic.Anthropic(api_key=api_key)


def moderate_vendor_text(
    vendor_text: str,
    model: str = ANTHROPIC_MODEL,
) -> Dict[str, Any]:
    """
    Moderate vendor notes or memo fields for inappropriate, harmful, or
    unsafe content using Anthropic's Claude model.

    Checks for hate speech, harassment, self-harm, sexual content, violence,
    and other policy violations.

    Args:
        vendor_text: The vendor notes or memo text to moderate.
        model: Anthropic model identifier (default: claude-3-5-sonnet-20241022).

    Returns:
        Dictionary with moderation results including:
            - safe: Boolean indicating if content is safe.
            - flags: List of flagged categories.
            - severity: Overall severity level (none, low, medium, high).
            - reasoning: Explanation of the moderation decision.
    """
    client = get_anthropic_client()

    system_prompt = (
        "You are a content safety moderation system. Analyze the provided text "
        "and determine if it contains any unsafe, harmful, or inappropriate content. "
        "Check for: hate speech, harassment, self-harm, sexual content, violence, "
        "profanity, spam, or policy violations. "
        "Return your analysis as a JSON object with exactly these keys: "
        "safe (boolean), flags (array of string categories), "
        "severity (one of: none, low, medium, high), "
        "reasoning (brief explanation string). "
        "Return ONLY the JSON object, no other text."
    )

    message = client.messages.create(
        model=model,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": f"Moderate the following vendor memo/notes text:\n\n{vendor_text}",
            }
        ],
        max_tokens=256,
        temperature=0.0,
    )

    response_text = message.content[0].text.strip()

    try:
        result = json.loads(response_text)
        return {
            "safe": result.get("safe", True),
            "flags": result.get("flags", []),
            "severity": result.get("severity", "none"),
            "reasoning": result.get("reasoning", ""),
            "model": model,
            "provider": "anthropic",
        }
    except json.JSONDecodeError:
        return {
            "safe": True,
            "flags": [],
            "severity": "none",
            "reasoning": f"Moderation analysis (raw): {response_text[:200]}",
            "model": model,
            "provider": "anthropic",
            "parse_error": True,
        }


def moderate_batch_vendor_texts(
    texts: List[str],
    model: str = ANTHROPIC_MODEL,
) -> List[Dict[str, Any]]:
    """
    Moderate a batch of vendor text fields sequentially.

    Args:
        texts: List of vendor notes/memo strings to moderate.
        model: Anthropic model identifier.

    Returns:
        List of moderation result dictionaries, one per input text.
    """
    results = []
    for text in texts:
        result = moderate_vendor_text(text, model=model)
        result["input_text_length"] = len(text)
        results.append(result)
    return results


def is_vendor_text_safe(
    vendor_text: str,
    model: str = ANTHROPIC_MODEL,
) -> bool:
    """
    Quick safety check for vendor text — returns True if content is safe.

    Args:
        vendor_text: The vendor notes or memo text to check.
        model: Anthropic model identifier.

    Returns:
        Boolean indicating if the text is safe.
    """
    result = moderate_vendor_text(vendor_text, model=model)
    return result.get("safe", True)
