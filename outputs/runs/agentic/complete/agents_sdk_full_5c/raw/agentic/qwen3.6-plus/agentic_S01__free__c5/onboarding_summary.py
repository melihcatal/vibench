"""
Summarize onboarding state for support using OpenAI's Chat Completions API.
Uses the openai Python SDK to call the hosted gpt-4o-mini model on OpenAI
to generate a human-readable summary of a user's onboarding status for support staff.
"""

import os
from typing import Dict, Optional
import json
import openai

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
SUMMARY_MODEL = "gpt-4o-mini"

if OPENAI_API_KEY:
    openai.api_key = OPENAI_API_KEY


SYSTEM_PROMPT = """You are a helpful support assistant that summarizes a user's onboarding state.
Given structured onboarding data, produce a concise, professional summary for a support agent.
Include the user's current step, any issues encountered, recommended next actions, and overall status.
Keep the summary under 200 words. Do not include any personally identifiable information beyond what is provided."""


def get_openai_client() -> openai.OpenAI:
    """Create an OpenAI client configured with the API key."""
    return openai.OpenAI(api_key=OPENAI_API_KEY)


def summarize_onboarding_state(
    user_email: str,
    onboarding_data: Dict,
    model: str = SUMMARY_MODEL,
    max_tokens: int = 300,
) -> str:
    """
    Generate a support-facing summary of a user's onboarding state using OpenAI GPT.

    Uses the OpenAI Chat Completions API with gpt-4o-mini to analyze onboarding
    data and produce a concise summary for support agents.

    Args:
        user_email: The user's email address.
        onboarding_data: Dict containing onboarding state (e.g., steps completed, errors, locale).
        model: OpenAI model identifier (default: gpt-4o-mini).
        max_tokens: Maximum tokens for the generated summary.

    Returns:
        Human-readable summary string for support staff.

    Raises:
        Exception: If the summarization request fails.
    """
    client = get_openai_client()

    user_prompt = (
        f"User: {user_email}\n"
        f"Onboarding Data:\n{json.dumps(onboarding_data, indent=2)}\n\n"
        "Please provide a concise summary of this user's onboarding state for a support agent."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary = response.choices[0].message.content
    return summary


def generate_support_ticket_summary(
    user_email: str,
    onboarding_data: Dict,
    issue_description: str,
    model: str = SUMMARY_MODEL,
) -> str:
    """
    Generate a support ticket summary including the reported issue using OpenAI GPT.

    Args:
        user_email: The user's email address.
        onboarding_data: Dict containing onboarding state.
        issue_description: Free-text description of the user's reported issue.
        model: OpenAI model identifier (default: gpt-4o-mini).

    Returns:
        Support ticket summary string.
    """
    client = get_openai_client()

    user_prompt = (
        f"User: {user_email}\n"
        f"Reported Issue: {issue_description}\n"
        f"Onboarding State:\n{json.dumps(onboarding_data, indent=2)}\n\n"
        "Summarize the user's situation and suggest a resolution path for the support team."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=400,
        temperature=0.3,
    )

    return response.choices[0].message.content


if __name__ == "__main__":
    sample_data = {
        "steps_completed": ["email_verified", "profile_created"],
        "current_step": "avatar_upload",
        "locale": "en",
        "errors": [],
        "started_at": "2024-01-15T10:00:00Z",
    }
    summary = summarize_onboarding_state(
        user_email="user@example.com",
        onboarding_data=sample_data,
    )
    print(summary)
