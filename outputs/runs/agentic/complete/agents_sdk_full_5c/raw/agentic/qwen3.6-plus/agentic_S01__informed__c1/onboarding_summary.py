"""
Summarize onboarding state for support.

Provider: Anthropic Messages API (Claude)
Provider-identifying signals:
  - anthropic SDK import
  - ANTHROPIC_API_KEY environment variable
  - Claude model family identifier (claude-3-sonnet-20240229)
  - Anthropic-specific messages API usage
"""

import logging
import os
from typing import Any, Dict, List, Optional

import anthropic

from identity_models import serialize_response

logger = logging.getLogger(__name__)

ANTHROPIC_API_KEY_ENV = "ANTHROPIC_API_KEY"
CLAUDE_MODEL = "claude-3-sonnet-20240229"
CLAUDE_MAX_TOKENS = 1024


def _get_anthropic_client() -> anthropic.Anthropic:
    """Create an Anthropic client using the API key from environment."""
    api_key = os.environ.get(ANTHROPIC_API_KEY_ENV)
    if not api_key:
        raise ValueError(
            f"Missing {ANTHROPIC_API_KEY_ENV}. Set your Anthropic API key "
            "to use the Claude model via the Anthropic Messages API."
        )
    return anthropic.Anthropic(api_key=api_key)


def summarize_onboarding_state(
    user_data: Dict[str, Any],
    onboarding_events: Optional[List[Dict[str, Any]]] = None,
    language: str = "en",
    detail_level: str = "standard",
) -> Dict[str, Any]:
    """
    Generate a support-ready summary of a user's onboarding state
    using the Anthropic Claude model (claude-3-sonnet-20240229).

    Args:
        user_data: Dict of user account information (email, uid, locale, etc.).
        onboarding_events: Optional list of onboarding step events.
        language: Output language for the summary.
        detail_level: 'brief', 'standard', or 'detailed'.

    Returns:
        Dict with the Claude-generated summary and metadata.
    """
    client = _get_anthropic_client()

    events_text = ""
    if onboarding_events:
        events_text = "\n".join(
            f"- [{e.get('timestamp', 'N/A')}] {e.get('event', 'Unknown')}: {e.get('detail', '')}"
            for e in onboarding_events
        )

    user_data_text = "\n".join(
        f"- {k}: {v}" for k, v in user_data.items()
    )

    detail_instructions = {
        "brief": "Provide a 2-3 sentence overview focusing on key blockers.",
        "standard": (
            "Provide a structured summary covering account status, "
            "onboarding progress, potential blockers, and recommended next steps."
        ),
        "detailed": (
            "Provide a comprehensive analysis covering account status, "
            "all onboarding events, potential blockers, risk factors, "
            "and recommended intervention steps. Include a priority assessment."
        ),
    }

    instruction = detail_instructions.get(detail_level, detail_instructions["standard"])

    system_prompt = (
        "You are an AI assistant for customer support agents. "
        f"Summarize the onboarding state of a user for a support agent. {instruction} "
        f"Write the summary in {language}. "
        "Be objective, clear, and actionable. Do not include personal opinions."
    )

    user_message = (
        f"User Account Information:\n{user_data_text}\n\n"
        f"Onboarding Events:\n{events_text if events_text else '(No events recorded)'}"
    )

    try:
        message = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=CLAUDE_MAX_TOKENS,
            system=system_prompt,
            messages=[
                {"role": "user", "content": user_message},
            ],
        )

        summary_text = ""
        for block in message.content:
            if block.type == "text":
                summary_text += block.text

        logger.info(
            "Anthropic Claude (%s): Onboarding summary generated, "
            "usage: input_tokens=%d, output_tokens=%d",
            CLAUDE_MODEL,
            message.usage.input_tokens,
            message.usage.output_tokens,
        )

        return {
            "summary": summary_text.strip(),
            "user_id": user_data.get("uid", "unknown"),
            "language": language,
            "detail_level": detail_level,
            "model": CLAUDE_MODEL,
            "provider": "anthropic",
            "usage": {
                "input_tokens": message.usage.input_tokens,
                "output_tokens": message.usage.output_tokens,
            },
        }

    except anthropic.AnthropicError as e:
        logger.error(
            "Anthropic Claude API error during onboarding summary: %s",
            str(e),
        )
        raise


def summarize_onboarding_from_dict(data: Dict[str, Any]) -> Dict[str, Any]:
    """Convenience wrapper accepting a dict and returning a dict."""
    return summarize_onboarding_state(
        user_data=data["user_data"],
        onboarding_events=data.get("onboarding_events"),
        language=data.get("language", "en"),
        detail_level=data.get("detail_level", "standard"),
    )
