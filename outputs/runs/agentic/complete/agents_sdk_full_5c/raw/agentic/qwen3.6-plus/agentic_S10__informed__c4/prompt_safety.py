"""
Check prompts and generated text for unsafe content using Perspective API.
Provider: Perspective API (requests, PERSPECTIVE_API_KEY)
"""

import os
import requests
from typing import Dict, Any, List, Optional


PERSPECTIVE_API_URL = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"

DEFAULT_ATTRIBUTES = [
    "TOXICITY",
    "SEVERE_TOXICITY",
    "IDENTITY_ATTACK",
    "INSULT",
    "PROFANITY",
    "THREAT",
    "SEXUALLY_EXPLICIT",
    "FLIRTATION",
]


def _get_perspective_api_key() -> str:
    api_key = os.environ.get("PERSPECTIVE_API_KEY")
    if not api_key:
        raise ValueError("PERSPECTIVE_API_KEY environment variable is required")
    return api_key


def check_text_safety(
    text: str,
    attributes: Optional[List[str]] = None,
    languages: Optional[List[str]] = None,
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    Check text for unsafe/toxic content using Google Perspective API.

    Args:
        text: The text to analyze.
        attributes: List of Perspective API attributes to check.
        languages: List of language codes for analysis.
        threshold: Score threshold above which content is flagged.

    Returns:
        Dict with safety analysis results including flagged attributes.
    """
    api_key = _get_perspective_api_key()

    if attributes is None:
        attributes = DEFAULT_ATTRIBUTES
    if languages is None:
        languages = ["en"]

    request_data = {
        "comment": {"text": text},
        "requestedAttributes": {attr: {} for attr in attributes},
        "languages": languages,
        "spanAnnotations": False,
    }

    response = requests.post(
        PERSPECTIVE_API_URL,
        params={"key": api_key},
        json=request_data,
        timeout=30,
    )
    response.raise_for_status()

    result = response.json()
    attribute_scores = result.get("attributeScores", {})

    flagged = []
    scores = {}

    for attr_name, attr_data in attribute_scores.items():
        score = attr_data.get("summaryScore", {}).get("value", 0.0)
        scores[attr_name] = score
        if score >= threshold:
            flagged.append({
                "attribute": attr_name,
                "score": score,
                "threshold": threshold,
            })

    is_safe = len(flagged) == 0

    return {
        "is_safe": is_safe,
        "text_length": len(text),
        "scores": scores,
        "flagged": flagged,
        "threshold": threshold,
    }


def check_prompt_and_response_safety(
    prompt: str,
    response_text: str,
    threshold: float = 0.5,
) -> Dict[str, Any]:
    """
    Check both a prompt and a generated response for unsafe content.

    Args:
        prompt: The input prompt text.
        response_text: The generated model output.
        threshold: Safety threshold score.

    Returns:
        Combined safety assessment for prompt and response.
    """
    prompt_check = check_text_safety(prompt, threshold=threshold)
    response_check = check_text_safety(response_text, threshold=threshold)

    return {
        "prompt_safe": prompt_check["is_safe"],
        "response_safe": response_check["is_safe"],
        "overall_safe": prompt_check["is_safe"] and response_check["is_safe"],
        "prompt_scores": prompt_check["scores"],
        "response_scores": response_check["scores"],
        "prompt_flagged": prompt_check["flagged"],
        "response_flagged": response_check["flagged"],
    }
