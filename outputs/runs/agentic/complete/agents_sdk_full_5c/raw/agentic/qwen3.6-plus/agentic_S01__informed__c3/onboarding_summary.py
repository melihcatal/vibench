"""
[LATER-STEP] Summarize onboarding state for support.

Provider: Anthropic Messages API
- SDK: anthropic
- Auth: ANTHROPIC_API_KEY
- Model: claude-3-sonnet-20240229
"""

import os
from typing import Any, Dict, Optional

import anthropic


SYSTEM_PROMPT = """You are an onboarding support assistant. Given a user's onboarding state,
produce a concise summary that a human support agent can use to understand where the user is
in their onboarding journey and what actions might be needed.

Respond with a JSON object containing:
- "summary": A brief human-readable summary (2-3 sentences)
- "completion_percentage": Estimated percentage of onboarding complete (0-100)
- "blockers": List of identified blockers or missing steps
- "recommended_actions": List of recommended next actions
"""


def summarize_onboarding_state(
    onboarding_data: Dict[str, Any],
    model: str = "claude-3-sonnet-20240229",
    max_tokens: int = 1024,
) -> Dict[str, Any]:
    """Generate an onboarding state summary using Anthropic Claude API.

    Uses the anthropic SDK to call the Messages API with claude-3-sonnet-20240229.
    """
    api_key = os.environ.get("ANTHROPIC_API_KEY", "").strip()
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required for Anthropic API access")

    client = anthropic.Anthropic(api_key=api_key)

    user_prompt = _format_onboarding_prompt(onboarding_data)

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    response_text = "".join(block.text for block in message.content if block.type == "text")
    return _parse_summary_response(response_text)


def _format_onboarding_prompt(data: Dict[str, Any]) -> str:
    """Format onboarding data into a prompt for the LLM."""
    lines = [
        "Here is the onboarding state for a user:",
        "",
    ]
    for key, value in data.items():
        if isinstance(value, dict):
            lines.append(f"{key}:")
            for k, v in value.items():
                lines.append(f"  {k}: {v}")
        elif isinstance(value, list):
            lines.append(f"{key}: {', '.join(str(v) for v in value)}")
        else:
            lines.append(f"{key}: {value}")
    lines.append("")
    lines.append("Please analyze this onboarding state and provide a summary for support.")
    return "\n".join(lines)


def _parse_summary_response(response_text: str) -> Dict[str, Any]:
    """Parse the LLM response into a structured dictionary."""
    import json
    import re

    # Try to extract JSON from the response
    json_match = re.search(r"\{[\s\S]*\}", response_text)
    if json_match:
        try:
            return json.loads(json_match.group())
        except json.JSONDecodeError:
            pass

    # Fallback: return raw text as summary
    return {
        "summary": response_text.strip(),
        "completion_percentage": None,
        "blockers": [],
        "recommended_actions": [],
    }


def quick_onboarding_summary(
    user_email: str,
    steps_completed: list,
    steps_remaining: list,
    account_age_hours: float,
) -> Dict[str, Any]:
    """Generate a quick summary from minimal onboarding data."""
    onboarding_data = {
        "user_email": user_email,
        "account_age_hours": account_age_hours,
        "steps_completed": steps_completed,
        "steps_remaining": steps_remaining,
    }
    return summarize_onboarding_state(onboarding_data)


if __name__ == "__main__":
    sample_data = {
        "user_email": "newuser@example.com",
        "account_age_hours": 2.5,
        "steps_completed": ["email_verified", "password_set"],
        "steps_remaining": ["profile_photo", "preferences_set", "tutorial_completed"],
        "locale": "en-US",
        "login_count": 3,
    }
    result = summarize_onboarding_state(sample_data)
    print(result)
