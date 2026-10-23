import json
from safety_client import get_openai_client, OPENAI_CHAT_MODEL
from safety_models import ModerationSummary


def summarize_moderation(results):
    total = len(results)
    flagged = sum(1 for r in results if r.flagged)
    allowed = total - flagged
    category_counts = {}
    category_score_sums = {}
    for r in results:
        cats = r.categories.to_dict()
        scores = r.category_scores.to_dict()
        for cat, is_flagged in cats.items():
            if is_flagged:
                category_counts[cat] = category_counts.get(cat, 0) + 1
            category_score_sums[cat] = category_score_sums.get(cat, 0.0) + scores.get(
                cat, 0.0
            )
    top_categories = dict(
        sorted(category_counts.items(), key=lambda x: x[1], reverse=True)[:5]
    )
    average_scores = {
        cat: round(total_sum / total, 4) if total > 0 else 0.0
        for cat, total_sum in category_score_sums.items()
    }
    flagged_texts = [r.text[:200] for r in results if r.flagged]
    client = get_openai_client()
    summary_prompt = (
        f"Summarize the following content moderation results in 2-3 sentences. "
        f"Total messages: {total}, Flagged: {flagged}, Allowed: {allowed}. "
        f"Top flagged categories: {json.dumps(top_categories)}. "
        f"Flagged content examples: {json.dumps(flagged_texts[:3])}. "
        f"Provide a concise moderation summary for a review team."
    )
    response = client.chat.completions.create(
        model=OPENAI_CHAT_MODEL,
        messages=[
            {
                "role": "system",
                "content": "You are a content moderation analyst. Provide concise, factual summaries of moderation decisions.",
            },
            {"role": "user", "content": summary_prompt},
        ],
        temperature=0.0,
        max_tokens=256,
    )
    summary_text = response.choices[0].message.content.strip()
    return ModerationSummary(
        total_messages=total,
        flagged_count=flagged,
        allowed_count=allowed,
        top_categories=top_categories,
        average_scores=average_scores,
        summary_text=summary_text,
    )


def summarize_flagged_only(results):
    flagged = [r for r in results if r.flagged]
    if not flagged:
        return ModerationSummary(
            total_messages=len(results),
            flagged_count=0,
            allowed_count=len(results),
            summary_text="No content was flagged during moderation.",
        )
    return summarize_moderation(flagged)


def generate_report(results):
    summary = summarize_moderation(results)
    report = summary.to_dict()
    report["flagged_items"] = [r.to_dict() for r in results if r.flagged]
    return report
