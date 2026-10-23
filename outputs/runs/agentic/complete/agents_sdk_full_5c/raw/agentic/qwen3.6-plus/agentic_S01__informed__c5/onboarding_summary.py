"""
onboarding_summary.py
Summarize onboarding state for support.

Provider: OpenAI Chat Completions (openai SDK)
Auth: OPENAI_API_KEY
Model: gpt-4o-mini
"""

import os
import json
from typing import Dict, Optional, List
from openai import OpenAI

# OpenAI configuration
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
ONBOARDING_MODEL = os.environ.get("ONBOARDING_MODEL_ID", "gpt-4o-mini")

SYSTEM_PROMPT = (
    "You are a helpful assistant that generates concise, structured summaries "
    "of user onboarding state for customer support teams. "
    "Summarize the key facts about the user's account, profile status, "
    "any issues encountered, and recommended next steps. "
    "Respond only with a JSON object matching the described schema."
)


def summarize_onboarding_state(
    user_data: Dict,
    onboarding_steps: List[Dict],
    issues: Optional[List[str]] = None,
    locale: Optional[str] = None,
) -> Dict:
    """
    Generate a summary of onboarding state for customer support using OpenAI GPT-4o-mini.

    Args:
        user_data: Dict containing user profile information (email, display_name, uid, etc.).
        onboarding_steps: List of step dicts with keys: step_name, status, timestamp.
        issues: Optional list of issue descriptions encountered during onboarding.
        locale: User's locale.

    Returns:
        Dict with summary containing: overview, account_status, completed_steps,
        pending_steps, issues_summary, recommended_actions.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY environment variable is not set.")

    client = OpenAI(api_key=OPENAI_API_KEY)

    steps_summary = json.dumps(onboarding_steps, indent=2)
    issues_summary = json.dumps(issues, indent=2) if issues else "No issues reported."
    user_info = json.dumps(user_data, indent=2)

    user_prompt = (
        f"User Information:\n{user_info}\n\n"
        f"Locale: {locale or 'en-US'}\n\n"
        f"Onboarding Steps:\n{steps_summary}\n\n"
        f"Issues:\n{issues_summary}\n\n"
        f"Generate a support-ready onboarding summary JSON with the following schema:\n"
        f'{{\n'
        f'  "overview": "Brief summary of the user\\'s onboarding journey",\n'
        f'  "account_status": "active | pending | flagged",\n'
        f'  "completed_steps": ["step1", "step2"],\n'
        f'  "pending_steps": ["step3", "step4"],\n'
        f'  "issues_summary": "Summary of any issues",\n'
        f'  "recommended_actions": ["Action 1", "Action 2"]\n'
        f"}}\n"
    )

    response = client.chat.completions.create(
        model=ONBOARDING_MODEL,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
        response_format={"type": "json_object"},
    )

    summary_text = response.choices[0].message.content
    summary_data = json.loads(summary_text)

    return summary_data


def get_onboarding_snapshot(
    uid: str,
    email: str,
    display_name: str,
) -> Dict:
    """
    Convenience function that creates a sample onboarding summary.

    Args:
        uid: User ID.
        email: User email.
        display_name: User display name.

    Returns:
        Summary dict from the OpenAI-powered summarization.
    """
    user_data = {
        "uid": uid,
        "email": email,
        "display_name": display_name,
        "created_at": "2024-01-15T10:30:00Z",
    }

    onboarding_steps = [
        {"step_name": "email_verification", "status": "completed", "timestamp": "2024-01-15T10:31:00Z"},
        {"step_name": "profile_setup", "status": "completed", "timestamp": "2024-01-15T10:35:00Z"},
        {"step_name": "preference_selection", "status": "pending", "timestamp": None},
        {"step_name": "first_login", "status": "pending", "timestamp": None},
    ]

    issues = ["Profile image upload failed on first attempt"]

    return summarize_onboarding_state(
        user_data=user_data,
        onboarding_steps=onboarding_steps,
        issues=issues,
        locale="en-US",
    )


if __name__ == "__main__":
    summary = get_onboarding_snapshot(
        uid="usr_abc123",
        email="support@example.com",
        display_name="Support User",
    )
    print(json.dumps(summary, indent=2))
