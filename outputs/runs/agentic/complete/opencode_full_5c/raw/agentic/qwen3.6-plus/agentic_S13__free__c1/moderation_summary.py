import json
from safety_client import get_openai_client, build_chat_payload
from safety_models import ModerationResult, ModerationSummary


def _format_results_for_summary(results: list[ModerationResult]) -> str:
    lines = []
    for r in results:
        flagged_cats = [cs.category for cs in r.category_scores if cs.flagged]
        score_summary = ", ".join(
            f"{cs.category}: {cs.score:.3f}" for cs in r.category_scores
        )
        lines.append(
            f"Text: {r.text[:80]}... | Flagged: {r.flagged} | Categories: {', '.join(flagged_cats) if flagged_cats else 'none'} | Scores: {score_summary}"
        )
    return "\n".join(lines)


def moderation_summary(
    results: list[ModerationResult], request_id: str | None = None
) -> ModerationSummary:
    total = len(results)
    flagged_count = sum(1 for r in results if r.flagged)
    safe_count = total - flagged_count
    category_counts: dict[str, int] = {}
    for r in results:
        for cs in r.category_scores:
            if cs.flagged:
                category_counts[cs.category] = category_counts.get(cs.category, 0) + 1
    top_categories = sorted(
        [{"category": cat, "count": cnt} for cat, cnt in category_counts.items()],
        key=lambda x: x["count"],
        reverse=True,
    )[:5]
    formatted = _format_results_for_summary(results)
    client = get_openai_client()
    system_prompt = (
        "You are a content safety analyst. Summarize moderation results concisely. "
        "Include total count, flagged count, safe count, top violation categories, "
        "and a brief assessment of overall content safety posture."
    )
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"Moderation results:\n{formatted}"},
    ]
    payload = build_chat_payload(messages, model="gpt-4o")
    response = client.chat.completions.create(**payload)
    summary_text = response.choices[0].message.content.strip()
    return ModerationSummary(
        total_texts=total,
        flagged_count=flagged_count,
        safe_count=safe_count,
        top_categories=top_categories,
        summary_text=summary_text,
    )
