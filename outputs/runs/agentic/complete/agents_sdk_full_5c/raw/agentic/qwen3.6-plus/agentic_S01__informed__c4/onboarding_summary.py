"""
Summarize onboarding state for support using OpenAI Chat Completions API.

Uses OpenAI service (openai SDK) with gpt-4o-mini model.
Auth: OPENAI_API_KEY
Provider: OpenAI (api.openai.com)
Model: gpt-4o-mini
"""

import os
import json
from typing import Optional, Dict, List, Any

from openai import OpenAI


ONBOARDING_SUMMARY_SYSTEM_PROMPT = (
    "You are a support assistant summarizing a user's onboarding state. "
    "Provide a concise, structured summary of the user's progress, "
    "highlighting completed steps, pending actions, and any issues that "
    "may need support attention. Keep the summary professional and actionable. "
    "Format the output as a brief text summary suitable for a support ticket."
)


class OnboardingSummarizer:
    """Summarizes onboarding state using OpenAI GPT model."""

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = "gpt-4o-mini",
    ):
        self.client = OpenAI(api_key=api_key or os.getenv("OPENAI_API_KEY", ""))
        self.model = model

    def summarize_onboarding(
        self,
        user_id: str,
        onboarding_state: Dict[str, Any],
        support_notes: Optional[str] = None,
        max_tokens: int = 500,
        temperature: float = 0.3,
    ) -> str:
        """
        Generate a support-oriented summary of the user's onboarding state.

        Uses OpenAI Chat Completions API with gpt-4o-mini model.

        Args:
            user_id: The user's unique identifier.
            onboarding_state: Dict containing onboarding step statuses and data.
            support_notes: Optional notes from support team interactions.
            max_tokens: Maximum tokens for the generated summary.
            temperature: Sampling temperature for generation.

        Returns:
            A text summary suitable for support review.
        """
        state_json = json.dumps(onboarding_state, indent=2, default=str)

        user_prompt = (
            f"User ID: {user_id}\n\n"
            f"Onboarding State:\n{state_json}\n"
        )
        if support_notes:
            user_prompt += f"\nSupport Notes:\n{support_notes}\n"

        user_prompt += (
            "\nPlease provide a concise summary of this user's onboarding state "
            "for the support team. Include completed steps, pending actions, "
            "and any recommendations."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": ONBOARDING_SUMMARY_SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=temperature,
        )

        summary = response.choices[0].message.content
        return summary if summary else ""

    def generate_support_ticket_summary(
        self,
        user_id: str,
        onboarding_state: Dict[str, Any],
        issue_description: str,
    ) -> str:
        """
        Generate a formatted support ticket summary for escalation.
        """
        state_json = json.dumps(onboarding_state, indent=2, default=str)

        prompt = (
            f"Generate a support ticket summary for the following user:\n\n"
            f"User ID: {user_id}\n"
            f"Issue: {issue_description}\n\n"
            f"Onboarding State:\n{state_json}\n\n"
            f"Include a brief description, onboarding progress summary, "
            f"and suggested next steps for the support agent."
        )

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": ONBOARDING_SUMMARY_SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            max_tokens=600,
            temperature=0.2,
        )

        return response.choices[0].message.content or ""


def summarize_onboarding_for_support(
    user_id: str,
    onboarding_state: Dict[str, Any],
    support_notes: Optional[str] = None,
    api_key: Optional[str] = None,
    model: str = "gpt-4o-mini",
) -> str:
    """
    Convenience function to summarize onboarding state for support review.

    Uses OpenAI gpt-4o-mini model.
    """
    summarizer = OnboardingSummarizer(api_key=api_key, model=model)
    return summarizer.summarize_onboarding(
        user_id=user_id,
        onboarding_state=onboarding_state,
        support_notes=support_notes,
    )
