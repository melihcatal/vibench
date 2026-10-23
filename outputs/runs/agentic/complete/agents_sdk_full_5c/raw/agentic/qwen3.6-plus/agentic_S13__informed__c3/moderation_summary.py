"""
Summarize moderation decisions using Anthropic Messages API.

Provider: Anthropic Messages API
SDK: anthropic
Model: claude-3-sonnet-20240229
"""

from typing import Any, Dict, List, Optional

import anthropic

from safety_models import BatchModerationResponse, ModerationResponse


def _build_moderation_context(
    results: List[ModerationResponse],
) -> str:
    """Format a list of moderation results into a human-readable context string."""
    lines = []
    for i, mod in enumerate(results, 1):
        lines.append(f"Message {i}: {mod.text!r}")
        for cat in mod.categories:
            lines.append(f"  - {cat.category}: severity={cat.severity}, flagged={cat.is_flagged}")
        lines.append(f"  Overall safe: {mod.is_safe}")
    return "\n".join(lines)


def summarize_moderation(
    moderation_results: List[ModerationResponse],
    api_key: Optional[str] = None,
    model: str = "claude-3-sonnet-20240229",
) -> str:
    """
    Use Anthropic's Claude model to generate a concise summary of
    moderation decisions for *moderation_results*.

    Provider: Anthropic Messages API
    Model: claude-3-sonnet-20240229
    """
    client = anthropic.Anthropic(api_key=api_key)

    context = _build_moderation_context(moderation_results)

    system_prompt = (
        "You are a content-moderation analyst. Given a list of moderation results "
        "for user-submitted messages, produce a brief executive summary that covers: "
        "(1) total messages reviewed, (2) number flagged as unsafe, (3) the top "
        "violation categories, and (4) any recommended follow-up actions. "
        "Keep the summary to 3-5 sentences."
    )

    user_prompt = (
        "Here are the moderation results:\n\n"
        f"{context}\n\n"
        "Provide the executive summary:"
    )

    message = client.messages.create(
        model=model,
        max_tokens=500,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    summary_text = ""
    for block in message.content:
        if block.type == "text":
            summary_text += block.text
    return summary_text


def summarize_batch_response(
    batch_response: BatchModerationResponse,
    api_key: Optional[str] = None,
    model: str = "claude-3-sonnet-20240229",
) -> str:
    """Convenience wrapper that accepts a BatchModerationResponse."""
    results = [r.moderation for r in batch_response.results]
    return summarize_moderation(results, api_key=api_key, model=model)


if __name__ == "__main__":
    sample_moderations = []
    summary = summarize_moderation(sample_moderations)
    print(summary)
