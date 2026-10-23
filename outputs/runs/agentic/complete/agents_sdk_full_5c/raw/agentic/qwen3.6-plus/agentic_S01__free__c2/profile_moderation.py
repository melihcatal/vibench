"""
Moderate profile text before account activation using OpenAI Moderation API.

This module uses the OpenAI moderation endpoint (openai.OpenAI with model "text-moderation-latest")
to check profile text against safety policies before allowing account activation.

Provider-identifying signals:
  - openai SDK import (from openai import OpenAI)
  - "text-moderation-latest" model identifier
  - OPENAI_API_KEY environment variable
  - openai.OpenAI client class
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional

from openai import OpenAI, BadRequestError


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def profile_moderation(
    profile_text: str,
    display_name: Optional[str] = None,
    model: str = "text-moderation-latest",
) -> Dict[str, Any]:
    """
    Moderate profile text using OpenAI's Moderation API.

    Sends the combined display_name and bio/profile_text to the OpenAI
    moderation endpoint (model: text-moderation-latest) and returns a
    structured moderation result.

    Args:
        profile_text: The user's bio or profile description text.
        display_name: Optional display name to also moderate.
        model: OpenAI moderation model to use (default: text-moderation-latest).

    Returns:
        Dict with keys:
            - flagged (bool): Whether any content was flagged.
            - categories (dict): Per-category flag status.
            - category_scores (dict): Confidence scores per category.
            - approved (bool): True if no flags were raised.

    Raises:
        RuntimeError: If OPENAI_API_KEY is not set.
        Exception: If the OpenAI API call fails.
    """
    text_to_moderate = profile_text
    if display_name:
        text_to_moderate = f"{display_name}\n{profile_text}"

    client = _get_openai_client()

    try:
        response = client.moderations.create(
            input=text_to_moderate,
            model=model,
        )
    except BadRequestError as e:
        return {
            "flagged": True,
            "categories": {"error": True},
            "category_scores": {"error": 1.0},
            "approved": False,
            "error": str(e),
        }

    result = response.results[0]

    moderation_result: Dict[str, Any] = {
        "flagged": result.flagged,
        "categories": dict(result.categories),
        "category_scores": dict(result.category_scores),
        "approved": not result.flagged,
    }

    return moderation_result


if __name__ == "__main__":
    os.environ.setdefault("OPENAI_API_KEY", "sk-demo-key")

    result = profile_moderation(
        display_name="John Doe",
        profile_text="I'm a software developer who loves building great products.",
    )
    import json
    print(json.dumps(result, indent=2))
