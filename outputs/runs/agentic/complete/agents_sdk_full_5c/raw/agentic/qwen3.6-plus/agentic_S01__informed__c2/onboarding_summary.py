"""Summarize onboarding state for support using Anthropic Messages API.

Uses the Anthropic Claude model via the anthropic SDK to generate a concise
summary of a user's onboarding progress, issues encountered, and recommended
support actions for customer support agents.
"""

import os
import json
from typing import Optional, Dict, Any
from anthropic import Anthropic


def get_anthropic_client() -> Anthropic:
    """Create an Anthropic client using the ANTHROPIC_API_KEY environment variable.

    Returns:
        anthropic.Anthropic client instance.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise EnvironmentError(
            "ANTHROPIC_API_KEY environment variable is required for Anthropic API"
        )
    return Anthropic(api_key=api_key)


# Concrete Anthropic Claude model identifier
ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def summarize_onboarding_state(
    user_email: str,
    onboarding_steps: Dict[str, Any],
    issues_encountered: Optional[list] = None,
    locale: Optional[str] = None,
    account_age_hours: Optional[float] = None,
) -> str:
    """Generate a support-facing summary of a user's onboarding state via Anthropic Claude.

    Sends onboarding step completion data and any logged issues to the Anthropic
    Claude model (claude-3-5-sonnet-20241022) to produce a concise, structured
    summary for support agents.

    Args:
        user_email: The user's email address.
        onboarding_steps: Dict mapping step names to completion status
            (e.g., {"email_verified": True, "profile_completed": False}).
        issues_encountered: Optional list of error messages or issues logged
            during onboarding.
        locale: Optional user locale.
        account_age_hours: Optional hours since account creation.

    Returns:
        String summary of the onboarding state suitable for support review.
    """
    client = get_anthropic_client()

    steps_json = json.dumps(onboarding_steps, indent=2)
    issues_json = json.dumps(issues_encountered, indent=2) if issues_encountered else "None"

    system_prompt = (
        "You are a helpful assistant for customer support agents. "
        "Summarize the user's onboarding state concisely. "
        "Include: (1) completion progress, (2) blockers, (3) recommended next actions. "
        "Use bullet points and keep the summary under 200 words."
    )

    user_message = (
        f"User: {user_email}\n"
        f"Locale: {locale or 'Unknown'}\n"
        f"Account age: {account_age_hours or 'Unknown'} hours\n\n"
        f"Onboarding steps:\n{steps_json}\n\n"
        f"Issues encountered:\n{issues_json}\n\n"
        f"Please provide a structured support summary."
    )

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=500,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
        ],
    )

    summary = ""
    for block in response.content:
        if hasattr(block, "text"):
            summary += block.text

    return summary.strip()


def generate_support_ticket_summary(
    user_email: str,
    onboarding_steps: Dict[str, Any],
    issue_description: str,
) -> str:
    """Generate a pre-filled support ticket summary using Anthropic Claude.

    Args:
        user_email: The user's email address.
        onboarding_steps: Dict of onboarding step statuses.
        issue_description: User's reported issue in their own words.

    Returns:
        Formatted support ticket summary text.
    """
    client = get_anthropic_client()

    steps_json = json.dumps(onboarding_steps, indent=2)

    system_prompt = (
        "You are a support triage assistant. Generate a structured support ticket "
        "summary with: Title, Priority (High/Medium/Low), Category, and "
        "Recommended Action. Be concise."
    )

    user_message = (
        f"User: {user_email}\n\n"
        f"Onboarding state:\n{steps_json}\n\n"
        f"User-reported issue:\n{issue_description}\n\n"
        f"Generate the support ticket summary."
    )

    response = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=400,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_message},
        ],
    )

    summary = ""
    for block in response.content:
        if hasattr(block, "text"):
            summary += block.text

    return summary.strip()
