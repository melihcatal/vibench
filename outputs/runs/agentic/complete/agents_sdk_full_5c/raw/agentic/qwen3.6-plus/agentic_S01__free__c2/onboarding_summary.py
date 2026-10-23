"""
Summarize onboarding state for support using OpenAI Chat Completions API.

This module uses the openai SDK (OpenAI with model "gpt-4o-mini") to generate
a concise, support-friendly summary of a user's onboarding state from structured data.

Provider-identifying signals:
  - openai SDK import (from openai import OpenAI)
  - "gpt-4o-mini" model identifier
  - OPENAI_API_KEY environment variable
  - openai.OpenAI client class
"""

from __future__ import annotations

import json
import os
from typing import Any, Dict, Optional

from openai import OpenAI


SYSTEM_PROMPT = (
    "You are a helpful support assistant. Summarize the user's onboarding state "
    "in 3-5 bullet points that a support agent can quickly understand. "
    "Include the user's email, locale, completed steps, any moderation issues, "
    "and overall onboarding progress. Be concise and factual."
)


def _get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
    return OpenAI(api_key=api_key)


def onboarding_summary(
    onboarding_state: Dict[str, Any],
    model: str = "gpt-4o-mini",
    max_tokens: int = 300,
) -> str:
    """
    Generate a support-ready summary of a user's onboarding state.

    Uses the OpenAI Chat Completions API with model gpt-4o-mini to produce
    a human-readable summary from structured onboarding data.

    Args:
        onboarding_state: Dict containing user onboarding data (uid, email,
            locale, steps_completed, moderation_status, notes, etc.).
        model: OpenAI model identifier (default: gpt-4o-mini).
        max_tokens: Maximum tokens for the generated summary.

    Returns:
        Generated summary string suitable for support ticketing systems.

    Raises:
        RuntimeError: If OPENAI_API_KEY is not set.
        Exception: If the OpenAI API call fails.
    """
    client = _get_openai_client()

    user_message = (
        "Summarize the following onboarding state for a support agent:\n\n"
        f"{json.dumps(onboarding_state, indent=2, default=str)}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary = response.choices[0].message.content or ""
    return summary


if __name__ == "__main__":
    os.environ.setdefault("OPENAI_API_KEY", "sk-demo-key")

    sample_state = {
        "uid": "abc123",
        "email": "user@example.com",
        "locale": "en-US",
        "steps_completed": ["registration", "email_verification", "profile_creation"],
        "moderation_status": "approved",
        "notes": "User completed onboarding without issues.",
    }

    result = onboarding_summary(sample_state)
    print(result)
