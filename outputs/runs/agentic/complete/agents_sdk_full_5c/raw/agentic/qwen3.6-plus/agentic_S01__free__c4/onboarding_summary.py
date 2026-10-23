"""
Summarize onboarding state for support staff.

Uses OpenAI's GPT-4o model to generate a concise summary of a user's
onboarding state, combining registration data, moderation results,
and locale preferences into support-friendly copy.
Provider: OpenAI (api.openai.com) with openai SDK.
"""

import json
import os
from typing import Any, Dict, List, Optional

import openai


def _get_openai_client() -> openai.OpenAI:
    """
    Build and return an OpenAI client configured with the API key
    from the OPENAI_API_KEY environment variable.

    Provider: OpenAI (api.openai.com)
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    return openai.OpenAI(api_key=api_key)


# OpenAI GPT-4o model identifier
ONBOARDING_SUMMARY_MODEL = "gpt-4o"


def onboarding_summary(
    user_data: Dict[str, Any],
    moderation_result: Optional[Dict[str, Any]] = None,
    locale: str = "en",
) -> str:
    """
    Generate a concise onboarding state summary for support staff
    using OpenAI's GPT-4o model.

    Provider: OpenAI (api.openai.com).
    The openai SDK import, OPENAI_API_KEY, and gpt-4o model identifier
    identify this as an OpenAI-specific integration.

    Args:
        user_data: Dict with user registration and profile data including
            keys like 'email', 'user_id', 'registration_date',
            'locale', 'email_verified', 'connection'.
        moderation_result: Optional moderation result dict with
            'is_safe', 'labels', 'overall_score'.
        locale: User's preferred locale code.

    Returns:
        A plain-text summary suitable for support ticket review.
    """
    client = _get_openai_client()

    system_prompt = (
        "You are a support assistant. Summarize a user's onboarding state "
        "concisely for a support agent. Include account status, any moderation "
        "flags, and recommended next steps. Keep it under 200 words. "
        "Use a professional tone."
    )

    user_context_parts = [f"User data: {json.dumps(user_data, default=str)}"]
    if moderation_result:
        user_context_parts.append(
            f"Moderation result: {json.dumps(moderation_result, default=str)}"
        )
    if locale != "en":
        user_context_parts.append(f"User locale: {locale}")

    user_prompt = " ".join(user_context_parts)

    response = client.chat.completions.create(
        model=ONBOARDING_SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=300,
    )

    summary = response.choices[0].message.content.strip()
    return summary


def onboarding_summary_batch(
    users_data: List[Dict[str, Any]],
    locale: str = "en",
) -> List[str]:
    """
    Generate summaries for multiple users in a single batch using
    OpenAI's GPT-4o model.

    Args:
        users_data: List of user data dicts.
        locale: Default locale for all users.

    Returns:
        List of summary strings, one per user.
    """
    client = _get_openai_client()

    system_prompt = (
        "You are a support assistant. For each user provided, generate a "
        "one-sentence onboarding summary noting account status and any flags."
    )

    users_json = json.dumps(users_data, default=str)
    user_prompt = f"Summarize onboarding for these {len(users_data)} users: {users_json}"

    response = client.chat.completions.create(
        model=ONBOARDING_SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary_text = response.choices[0].message.content.strip()
    # Split by numbered lines if present, otherwise return as single summary
    lines = [
        line.strip()
        for line in summary_text.split("\n")
        if line.strip()
    ]
    return lines if lines else [summary_text]
