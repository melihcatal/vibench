import json
import anthropic
from safety_models import BatchModerationResult, ModerationResult

ANTHROPIC_MODEL = "claude-3-5-sonnet-20241022"


def _build_moderation_context(results: BatchModerationResult) -> str:
    lines = []
    lines.append(
        f"Moderation batch summary: {results.total_flagged} flagged out of {len(results.results)} total."
    )
    lines.append("")
    for i, r in enumerate(results.results):
        status = "FLAGGED" if r.overall_flagged else "SAFE"
        lines.append(f"Message {i + 1} [{status}]: {r.text[:120]}")
        for cat in r.categories:
            lines.append(
                f"  - {cat.category}: {cat.severity} (value={cat.severity_value}, flagged={cat.flagged})"
            )
        if r.blocklist_matches:
            for bl in r.blocklist_matches:
                lines.append(
                    f"  - Blocklist match: {bl.get('blocklist_name', 'unknown')}"
                )
        lines.append("")
    return "\n".join(lines)


def moderation_summary(
    batch_result: BatchModerationResult,
    api_key: str | None = None,
    model: str = ANTHROPIC_MODEL,
) -> dict:
    client = anthropic.Anthropic(api_key=api_key)
    context = _build_moderation_context(batch_result)
    system_prompt = (
        "You are a content moderation analyst. Summarize the moderation decisions provided. "
        "Return a JSON object with keys: executive_summary, risk_assessment, recommended_actions, and category_breakdown."
    )
    user_prompt = f"Here are the moderation results:\n\n{context}\n\nProvide a structured summary."
    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    summary_text = message.content[0].text
    try:
        summary_json = json.loads(summary_text)
    except json.JSONDecodeError:
        summary_json = {"raw_summary": summary_text}
    summary_json["total_messages"] = len(batch_result.results)
    summary_json["flagged_count"] = batch_result.total_flagged
    summary_json["safe_count"] = batch_result.total_safe
    return summary_json


def summarize_single_result(
    result: ModerationResult,
    api_key: str | None = None,
    model: str = ANTHROPIC_MODEL,
) -> str:
    client = anthropic.Anthropic(api_key=api_key)
    cat_details = ", ".join(f"{c.category}={c.severity}" for c in result.categories)
    user_prompt = (
        f"Moderation result for text: {result.text[:200]}\n"
        f"Categories: {cat_details}\n"
        f"Highest severity: {result.highest_severity}\n"
        f"Overall flagged: {result.overall_flagged}\n\n"
        "Provide a one-sentence summary of this moderation decision."
    )
    message = client.messages.create(
        model=model,
        max_tokens=256,
        messages=[{"role": "user", "content": user_prompt}],
    )
    return message.content[0].text
