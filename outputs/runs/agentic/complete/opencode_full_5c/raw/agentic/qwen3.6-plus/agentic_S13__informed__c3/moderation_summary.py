import os

import anthropic

from safety_models import ThresholdDecision, SafetyResponse, BatchSafetyResponse

ANTHROPIC_MODEL = "claude-sonnet-4-20250514"


def summarize_moderation_decisions(
    decisions: list[ThresholdDecision],
    api_key: str | None = None,
) -> str:
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    client = anthropic.Anthropic(api_key=api_key)

    decision_details = []
    for d in decisions:
        violated = ", ".join(c.value for c in d.violated_categories)
        exceeded = ", ".join(
            f"{k.value}={v.name}" for k, v in d.exceeded_thresholds.items()
        )
        decision_details.append(
            f"Text: {d.text[:100]}... | Allowed: {d.allowed} | "
            f"Violated: {violated} | Exceeded: {exceeded}"
        )

    summary_prompt = (
        "Summarize the following content moderation decisions. "
        "Provide a concise overview of patterns, most common violations, "
        "and overall risk assessment.\n\n"
        "Decisions:\n" + "\n".join(decision_details)
    )

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=512,
        temperature=0.3,
        system="You are a content moderation analyst summarizing safety decisions.",
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return message.content[0].text


def summarize_batch_moderation(
    batch_response: BatchSafetyResponse,
    api_key: str | None = None,
) -> str:
    if api_key is None:
        api_key = os.environ.get("ANTHROPIC_API_KEY", "")

    client = anthropic.Anthropic(api_key=api_key)

    blocked = [r for r in batch_response.results if r.response.block_action]
    allowed = [r for r in batch_response.results if not r.response.block_action]

    summary_prompt = (
        f"Total messages analyzed: {batch_response.total_processed}\n"
        f"Blocked: {len(blocked)}\n"
        f"Allowed: {len(allowed)}\n\n"
        "Provide a brief summary of the moderation outcomes, "
        "highlighting the main safety concerns found."
    )

    message = client.messages.create(
        model=ANTHROPIC_MODEL,
        max_tokens=256,
        temperature=0.2,
        system="You are a content moderation analyst.",
        messages=[{"role": "user", "content": summary_prompt}],
    )

    return message.content[0].text


def generate_moderation_report(
    decisions: list[ThresholdDecision],
    api_key: str | None = None,
) -> dict:
    summary_text = summarize_moderation_decisions(decisions, api_key)

    blocked_count = sum(1 for d in decisions if not d.allowed)
    allowed_count = sum(1 for d in decisions if d.allowed)

    category_counts = {}
    for d in decisions:
        for cat in d.violated_categories:
            category_counts[cat.value] = category_counts.get(cat.value, 0) + 1

    return {
        "summary": summary_text,
        "total_decisions": len(decisions),
        "blocked_count": blocked_count,
        "allowed_count": allowed_count,
        "category_violation_counts": category_counts,
    }
