"""
Summarize moderation decisions for review.
Provider: Anthropic Messages API (Claude)
"""

import os
from typing import Optional, List, Dict

import anthropic


DEFAULT_MODEL = "claude-3-5-sonnet-20241022"


def _get_anthropic_client() -> anthropic.Anthropic:
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    return anthropic.Anthropic(api_key=api_key)


def summarize_moderation_decisions(
    decisions: List[Dict],
    model: str = DEFAULT_MODEL,
    max_tokens: int = 1024,
    temperature: float = 0.3,
) -> str:
    """
    Summarize a list of moderation decisions using Anthropic Claude.

    Each decision dict should contain keys like 'text', 'categories',
    'overall_safe', 'allowed', etc. as produced by the safety modules.

    Args:
        decisions: List of moderation decision dicts.
        model: Anthropic model identifier (default: claude-3-5-sonnet-20241022).
        max_tokens: Maximum tokens in the summary response.
        temperature: Sampling temperature for generation.

    Returns:
        Human-readable summary string of moderation decisions.
    """
    client = _get_anthropic_client()

    decisions_formatted = []
    for i, d in enumerate(decisions, 1):
        text_preview = str(d.get("text", ""))[:200]
        overall = d.get("overall_safe", "unknown")
        allowed = d.get("allowed", "unknown")
        cats = d.get("categories", [])
        cat_details = ", ".join(
            f"{c.get('category', '?')}: severity {c.get('severity', 0)} ({c.get('severity_label', '?')})"
            for c in cats
        ) if isinstance(cats, list) else str(cats)

        decisions_formatted.append(
            f"Decision {i}:\n"
            f"  Text: {text_preview}\n"
            f"  Overall Safe: {overall}\n"
            f"  Allowed: {allowed}\n"
            f"  Categories: {cat_details}\n"
        )

    decisions_text = "\n".join(decisions_formatted)

    system_prompt = (
        "You are a content moderation summarizer. Review the moderation decisions "
        "provided and produce a concise executive summary highlighting patterns, "
        "overall safety trends, notable violations, and recommended actions."
    )

    user_prompt = (
        f"Please summarize the following {len(decisions)} moderation decisions:\n\n"
        f"{decisions_text}"
    )

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        temperature=temperature,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt},
        ],
    )

    summary = ""
    for block in message.content:
        if hasattr(block, 'text') and block.text:
            summary += block.text

    return summary


def summarize_with_stats(
    decisions: List[Dict],
    model: str = DEFAULT_MODEL,
) -> Dict:
    """
    Produce both a summary and basic statistics.

    Args:
        decisions: List of moderation decision dicts.
        model: Anthropic model identifier.

    Returns:
        Dict with 'summary', 'total', 'safe_count', 'unsafe_count'.
    """
    total = len(decisions)
    safe_count = sum(1 for d in decisions if d.get("overall_safe", False))
    unsafe_count = total - safe_count

    summary = summarize_moderation_decisions(decisions, model=model)

    return {
        "summary": summary,
        "total": total,
        "safe_count": safe_count,
        "unsafe_count": unsafe_count,
    }
