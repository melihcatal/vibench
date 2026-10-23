"""
[LATER-STEP] moderation_summary.py - Summarize moderation decisions
using Mistral Chat API.

Provider: Mistral
SDK: mistralai
Auth: MISTRAL_API_KEY
"""

import json
import os
from typing import Optional

from mistralai import Mistral

MISTRAL_MODEL = "mistral-large-latest"


def summarize_moderation_decisions(
    decisions: list[dict],
    api_key: Optional[str] = None,
    max_tokens: int = 500,
) -> str:
    """
    Generate a concise summary of a list of moderation decisions
    using the Mistral Chat API (mistral-large-latest model).

    Args:
        decisions: List of dicts, each with keys like 'text_preview',
                   'allowed', 'max_severity', 'action', 'category_scores'.
        api_key: Optional Mistral API key override.
        max_tokens: Maximum tokens in the summary.

    Returns:
        A text summary of the moderation decisions.
    """
    key = api_key or os.environ.get("MISTRAL_API_KEY", "")
    client = Mistral(api_key=key)

    decisions_json = json.dumps(decisions, indent=2, default=str)

    system_prompt = (
        "You are a moderation policy assistant. "
        "Summarize the following moderation decisions. "
        "Include the total count, how many were allowed vs blocked, "
        "the most common violation categories, and any notable patterns. "
        "Keep the summary concise and actionable."
    )

    user_prompt = f"Moderation decisions:\n{decisions_json}"

    response = client.chat.complete(
        model=MISTRAL_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
    )

    summary = response.choices[0].message.content
    return summary or "No summary generated."


def generate_summary_report(
    decisions: list[dict],
    report_title: str = "Moderation Summary Report",
) -> dict:
    """
    Generate a full summary report with metadata and the Mistral-generated summary.
    """
    summary_text = summarize_moderation_decisions(decisions)
    total = len(decisions)
    allowed = sum(1 for d in decisions if d.get("allowed", True))
    blocked = total - allowed

    return {
        "title": report_title,
        "total_items": total,
        "allowed_count": allowed,
        "blocked_count": blocked,
        "summary": summary_text,
        "model_used": MISTRAL_MODEL,
    }


if __name__ == "__main__":
    sample_decisions = [
        {"text_preview": "Sample message 1", "allowed": True, "max_severity": 1, "action": "allow", "category_scores": {"hate": 1}},
        {"text_preview": "Sample message 2", "allowed": False, "max_severity": 6, "action": "block", "category_scores": {"violence": 6}},
    ]
    report = generate_summary_report(sample_decisions)
    print(report)
