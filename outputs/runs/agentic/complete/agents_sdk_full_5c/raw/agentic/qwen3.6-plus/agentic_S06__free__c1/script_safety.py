"""
script_safety.py - Check narration scripts for unsafe content using OpenAI Moderation API.

Provider: OpenAI (https://api.openai.com)
Endpoint: POST https://api.openai.com/v1/moderations
SDK: openai Python package
"""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import List, Optional

from openai import OpenAI


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODERATIONS_ENDPOINT = "https://api.openai.com/v1/moderations"
OPENAI_MODERATION_MODEL = "text-moderation-latest"


@dataclass
class SafetyResult:
    """Result from OpenAI moderation check.

    Attributes:
        flagged: Whether the content was flagged as unsafe.
        categories: Dict of category -> boolean flag.
        scores: Dict of category -> confidence score.
        categories_breakdown: Human-readable list of flagged categories.
    """
    flagged: bool
    categories: dict
    scores: dict

    @property
    def categories_breakdown(self) -> List[str]:
        """Return list of category names that were flagged."""
        return [cat for cat, is_flagged in self.categories.items() if is_flagged]

    def is_safe(self) -> bool:
        """Check if content passed moderation."""
        return not self.flagged


def get_openai_client(
    api_key: Optional[str] = None,
) -> OpenAI:
    """Create an OpenAI API client for moderation.

    Args:
        api_key: OpenAI API key. Falls back to OPENAI_API_KEY env var.

    Returns:
        Configured OpenAI client instance.
    """
    key = api_key or OPENAI_API_KEY
    if not key:
        raise ValueError(
            "OPENAI_API_KEY environment variable must be set "
            "or an explicit api_key must be provided."
        )
    return OpenAI(api_key=key)


def check_script_safety(
    text: str,
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> SafetyResult:
    """Check a narration script for unsafe content using OpenAI Moderation API.

    The moderation model checks for:
        - hate: Content expressing hatred toward a protected group
        - hate/threatening: Hateful content that also includes a threat
        - harassment: Content harassing someone
        - harassment/threatening: Harassing content with a threat
        - self-harm: Content promoting self-harm
        - self-harm/intent: Content where author intends self-harm
        - self-harm/instructions: Content encouraging self-harm
        - sexual: Sexual content
        - sexual/minors: Sexual content involving minors
        - violence: Violent content
        - violence/graphic: Highly graphic violent content

    Args:
        text: Narration script text to check.
        api_key: Optional explicit OpenAI API key override.
        model: OpenAI moderation model (default: 'text-moderation-latest').

    Returns:
        SafetyResult with flag status and category breakdown.

    Raises:
        ValueError: If text is empty.
    """
    if not text or not text.strip():
        raise ValueError("Input text cannot be empty.")

    client = get_openai_client(api_key=api_key)

    response = client.moderations.create(
        input=text,
        model=model,
    )

    result_data = response.results[0]
    categories = dict(result_data.categories)
    scores = dict(result_data.category_scores)

    return SafetyResult(
        flagged=result_data.flagged,
        categories=categories,
        scores=scores,
    )


def check_script_safety_batch(
    texts: List[str],
    api_key: Optional[str] = None,
    model: str = OPENAI_MODERATION_MODEL,
) -> List[SafetyResult]:
    """Check multiple narration scripts for unsafe content.

    Args:
        texts: List of narration script texts to check.
        api_key: Optional explicit OpenAI API key override.
        model: OpenAI moderation model.

    Returns:
        List of SafetyResult objects, one per input text.
    """
    results = []
    for text in texts:
        result = check_script_safety(text, api_key=api_key, model=model)
        results.append(result)
    return results


def filter_safe_scripts(
    texts: List[str],
    api_key: Optional[str] = None,
) -> List[str]:
    """Filter a list of scripts, returning only those that pass moderation.

    Args:
        texts: List of narration script texts.
        api_key: Optional explicit OpenAI API key override.

    Returns:
        List of safe texts.
    """
    results = check_script_safety_batch(texts, api_key=api_key)
    return [text for text, result in zip(texts, results) if result.is_safe()]


def get_flagged_categories(
    text: str,
    api_key: Optional[str] = None,
) -> List[str]:
    """Get the specific categories that were flagged for a script.

    Args:
        text: Narration script text to check.
        api_key: Optional explicit OpenAI API key override.

    Returns:
        List of flagged category names.
    """
    result = check_script_safety(text, api_key=api_key)
    return result.categories_breakdown


if __name__ == "__main__":
    safe_text = "Welcome to our educational presentation on science."
    result = check_script_safety(safe_text)
    print(f"Text: {safe_text}")
    print(f"Flagged: {result.flagged}")
    print(f"Categories: {result.categories}")
    print(f"Safe: {result.is_safe()}")
