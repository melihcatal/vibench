"""
Summarize onboarding state for support using OpenAI Chat Completion API.
Provider: OpenAI Chat Completions API (openai package)
"""

import os
import json
from typing import Dict, Any, Optional, List
from datetime import datetime

import openai


OPENAI_CHAT_MODEL_ID = "gpt-4o-mini"


def summarize_onboarding_state(
    user_id: str,
    onboarding_steps: List[Dict[str, Any]],
    profile_data: Optional[Dict[str, Any]] = None,
    support_notes: Optional[str] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a concise summary of user onboarding state for support team review.

    Args:
        user_id: The user's unique identifier
        onboarding_steps: List of step dicts with name, status, timestamp
        profile_data: Optional profile information
        support_notes: Optional existing support notes
        api_key: OpenAI API key (falls back to OPENAI_API_KEY env var)

    Returns:
        Dict with summary text and metadata
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return _error_summary("OpenAI API key not configured")

    context = _build_onboarding_context(
        user_id=user_id,
        onboarding_steps=onboarding_steps,
        profile_data=profile_data,
        support_notes=support_notes,
    )

    system_prompt = (
        "You are a support assistant. Summarize the user's onboarding state "
        "concisely for a support agent. Highlight any blockers, incomplete steps, "
        "and suggest next actions. Keep the summary under 150 words."
    )

    client = openai.OpenAI(api_key=key)

    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ],
            temperature=0.3,
            max_tokens=300,
        )

        summary_text = response.choices[0].message.content.strip()

        completion_tokens = response.usage.completion_tokens if response.usage else 0
        prompt_tokens = response.usage.prompt_tokens if response.usage else 0

        return {
            "user_id": user_id,
            "summary": summary_text,
            "completion_tokens": completion_tokens,
            "prompt_tokens": prompt_tokens,
            "model": OPENAI_CHAT_MODEL_ID,
            "provider": "openai_chat_completions",
            "success": True,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except openai.APIError as exc:
        return _error_summary(f"OpenAI API error: {str(exc)}")
    except openai.RateLimitError:
        return _error_summary("OpenAI rate limit exceeded")
    except openai.AuthenticationError:
        return _error_summary("OpenAI authentication failed")
    except Exception as exc:
        return _error_summary(f"Unexpected error: {str(exc)}")


def generate_support_ticket_summary(
    user_id: str,
    onboarding_steps: List[Dict[str, Any]],
    issue_description: str,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a support ticket summary with onboarding context.

    Args:
        user_id: User identifier
        onboarding_steps: List of onboarding steps
        issue_description: User's reported issue
        api_key: OpenAI API key

    Returns:
        Dict with ticket summary
    """
    key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not key:
        return _error_summary("OpenAI API key not configured")

    context = _build_onboarding_context(user_id, onboarding_steps)
    context += f"\n\nUser reported issue: {issue_description}"

    system_prompt = (
        "You are a support ticket assistant. Create a concise ticket summary "
        "including the user's onboarding status and their reported issue. "
        "Suggest a priority level (low/medium/high) and initial troubleshooting steps."
    )

    client = openai.OpenAI(api_key=key)

    try:
        response = client.chat.completions.create(
            model=OPENAI_CHAT_MODEL_ID,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": context},
            ],
            temperature=0.2,
            max_tokens=250,
        )

        ticket_summary = response.choices[0].message.content.strip()

        return {
            "user_id": user_id,
            "ticket_summary": ticket_summary,
            "model": OPENAI_CHAT_MODEL_ID,
            "provider": "openai_chat_completions",
            "success": True,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }

    except openai.APIError as exc:
        return _error_summary(f"OpenAI API error: {str(exc)}")
    except Exception as exc:
        return _error_summary(f"Unexpected error: {str(exc)}")


def _build_onboarding_context(
    user_id: str,
    onboarding_steps: List[Dict[str, Any]],
    profile_data: Optional[Dict[str, Any]] = None,
    support_notes: Optional[str] = None,
) -> str:
    """Build context string from onboarding data."""
    lines = [f"User ID: {user_id}", "", "Onboarding Steps:"]

    for step in onboarding_steps:
        status = step.get("status", "unknown")
        name = step.get("name", "unnamed")
        timestamp = step.get("timestamp", "")
        lines.append(f"  - {name}: {status}{' (' + timestamp + ')' if timestamp else ''}")

    if profile_data:
        lines.append("\nProfile Data:")
        for key, value in profile_data.items():
            lines.append(f"  {key}: {value}")

    if support_notes:
        lines.append(f"\nSupport Notes: {support_notes}")

    return "\n".join(lines)


def _error_summary(error_message: str) -> Dict[str, Any]:
    """Return an error summary result."""
    return {
        "user_id": None,
        "summary": None,
        "model": OPENAI_CHAT_MODEL_ID,
        "provider": "openai_chat_completions",
        "success": False,
        "error": error_message,
        "timestamp": datetime.utcnow().isoformat() + "Z",
    }


if __name__ == "__main__":
    sample_steps = [
        {"name": "Account Created", "status": "completed", "timestamp": "2024-01-15T10:00:00Z"},
        {"name": "Email Verified", "status": "completed", "timestamp": "2024-01-15T10:05:00Z"},
        {"name": "Profile Setup", "status": "in_progress", "timestamp": ""},
        {"name": "Terms Accepted", "status": "pending", "timestamp": ""},
    ]

    result = summarize_onboarding_state(
        user_id="usr_12345",
        onboarding_steps=sample_steps,
        profile_data={"display_name": "Test User", "locale": "en-US"},
    )
    if result["success"]:
        print(f"Summary for {result['user_id']}:\n{result['summary']}")
    else:
        print(f"Error: {result['error']}")
