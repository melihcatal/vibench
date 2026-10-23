"""Summarizes a list of moderation decisions using Anthropic Claude."""
from typing import List
from safety_client import get_anthropic_client
from safety_models import ModerationDecision, ModerationSummary


def summarize_moderation_decisions(decisions: List[ModerationDecision]) -> ModerationSummary:
    """
    Summarizes a list of moderation decisions using Anthropic's Claude model.

    Args:
        decisions: A list of moderation decision objects.

    Returns:
        A summary object containing statistics and a textual summary.
    """
    client = get_anthropic_client()

    total_reviews = len(decisions)
    total_blocked = sum(1 for d in decisions if d.decision == "blocked")
    category_counts = {}
    for d in decisions:
        for cat in d.categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1

    prompt_text = "Here are the moderation decisions for the last hour:\n\n"
    for d in decisions:
        prompt_text += (
            f"- ID: {d.text_id}, Decision: {d.decision}, "
            f"Categories: {', '.join(d.categories)}, Rationale: {d.rationale}\n"
        )
    prompt_text += "\nPlease provide a brief, professional summary of these moderation activities."

    message = client.messages.create(
        model="claude-3-sonnet-20240229",
        max_tokens=512,
        messages=[
            {"role": "user", "content": prompt_text}
        ]
    )
    
    summary_text = message.content[0].text if message.content else "Could not generate summary."

    return ModerationSummary(
        total_reviews=total_reviews,
        total_blocked=total_blocked,
        category_counts=category_counts,
        summary_text=summary_text,
    )
