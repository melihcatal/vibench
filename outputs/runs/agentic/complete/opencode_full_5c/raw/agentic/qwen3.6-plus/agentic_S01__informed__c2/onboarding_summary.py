import os
import json
from typing import Dict, List, Optional, Any
from anthropic import Anthropic

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = "claude-sonnet-4-20250514"

SYSTEM_PROMPT = (
    "You are a support assistant. Summarize the onboarding state of a user "
    "based on the provided metadata. Keep the summary concise and actionable. "
    "Include any flags, issues, or items that require support attention."
)


def summarize_onboarding_state(
    user_id: str,
    onboarding_data: Dict[str, Any],
    max_tokens: int = 512,
    model: Optional[str] = None,
) -> str:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    model_id = model or ANTHROPIC_MODEL
    payload = json.dumps(onboarding_data, default=str)
    message = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"User ID: {user_id}\n\n"
                    f"Onboarding metadata:\n{payload}\n\n"
                    f"Please provide a concise summary of this user's onboarding state for support review."
                ),
            },
        ],
    )
    summary = ""
    for block in message.content:
        if hasattr(block, "text"):
            summary += block.text
    return summary


def summarize_onboarding_with_moderation_flags(
    user_id: str,
    onboarding_data: Dict[str, Any],
    moderation_results: Optional[List[Dict[str, Any]]] = None,
    max_tokens: int = 512,
    model: Optional[str] = None,
) -> str:
    client = Anthropic(api_key=ANTHROPIC_API_KEY)
    model_id = model or ANTHROPIC_MODEL
    data_section = json.dumps(onboarding_data, default=str)
    moderation_section = ""
    if moderation_results:
        moderation_section = json.dumps(moderation_results, default=str)
    message = client.messages.create(
        model=model_id,
        max_tokens=max_tokens,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": (
                    f"User ID: {user_id}\n\n"
                    f"Onboarding metadata:\n{data_section}\n\n"
                    f"Moderation results:\n{moderation_section}\n\n"
                    f"Please provide a concise summary of this user's onboarding state for support review, "
                    f"highlighting any moderation concerns."
                ),
            },
        ],
    )
    summary = ""
    for block in message.content:
        if hasattr(block, "text"):
            summary += block.text
    return summary
