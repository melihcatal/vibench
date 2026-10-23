"""Summarize moderation decisions using OpenAI GPT-4o for summarization."""

import json
import os
from typing import Dict, List

from openai import OpenAI


def summarize_moderation_decisions(
    decisions: List[Dict[str, str | float | bool]],
    model: str = "gpt-4o",
) -> str:
    """Summarize a list of moderation decisions into a concise review-ready report.

    Uses OpenAI's gpt-4o model via api.openai.com to generate natural-language
    summaries of batch moderation outcomes, including flagged categories,
    severity patterns, and recommended actions.

    Args:
        decisions: List of dicts, each containing keys like 'text_preview',
            'flagged', 'categories', 'category_scores'.
        model: OpenAI model to use (default: gpt-4o).

    Returns:
        String summary of moderation decisions.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    decisions_json = json.dumps(decisions, indent=2, default=str)

    system_prompt = (
        "You are a content safety analyst. Summarize the provided moderation decisions "
        "into a concise report. Include: total messages reviewed, number flagged, "
        "most common violation categories, severity trends, and recommended actions. "
        "Use clear bullet points and keep the summary under 300 words."
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Moderation decisions to summarize:\n{decisions_json}"},
        ],
        temperature=0.2,
        max_tokens=500,
    )

    summary = response.choices[0].message.content or ""
    return summary


def summarize_single_decision(
    decision: Dict[str, str | float | bool],
    model: str = "gpt-4o",
) -> str:
    """Summarize a single moderation decision into a reviewer note.

    Uses OpenAI's gpt-4o model on api.openai.com.

    Args:
        decision: Dict with 'text_preview', 'flagged', 'categories', 'category_scores'.
        model: OpenAI model identifier (default: gpt-4o).

    Returns:
        String summary for a single decision.
    """
    api_key = os.environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a content moderation assistant. Given a single moderation decision, "
        "write a brief one-paragraph reviewer note explaining why the content was "
        "flagged or allowed, referencing the specific categories and confidence scores."
    )

    decision_json = json.dumps(decision, indent=2, default=str)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": f"Decision to summarize:\n{decision_json}"},
        ],
        temperature=0.2,
        max_tokens=200,
    )

    return response.choices[0].message.content or ""


if __name__ == "__main__":
    sample_decisions = [
        {
            "text_preview": "Hello world",
            "flagged": False,
            "categories": {"hate": False, "self-harm": False},
            "category_scores": {"hate": 0.01, "self-harm": 0.02},
        },
        {
            "text_preview": "[REDACTED]",
            "flagged": True,
            "categories": {"hate": True, "violence": True},
            "category_scores": {"hate": 0.92, "violence": 0.85},
        },
    ]
    result = summarize_moderation_decisions(sample_decisions)
    print(result)
