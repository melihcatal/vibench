from safety_client import call_chat, OPENAI_CHAT_MODEL
from safety_models import ModerationSummary


def summarize_moderation_decisions(decisions, model=None):
    decision_entries = []
    category_counts = {}
    top_violations = []

    for idx, decision in enumerate(decisions):
        flagged = decision.get("flagged", False)
        categories = decision.get("categories", [])
        scores = decision.get("category_scores", [])

        for cat in categories:
            category_counts[cat] = category_counts.get(cat, 0) + 1

        if flagged:
            max_score = 0.0
            max_cat = "unknown"
            for s in scores:
                if s.get("score", 0) > max_score:
                    max_score = s["score"]
                    max_cat = s["name"]
            top_violations.append(
                {
                    "index": idx,
                    "primary_category": max_cat,
                    "score": max_score,
                    "all_categories": categories,
                }
            )

    top_violations.sort(key=lambda x: x["score"], reverse=True)
    top_violations = top_violations[:10]

    total_analyzed = len(decisions)
    total_flagged = sum(1 for d in decisions if d.get("flagged", False))
    total_allowed = total_analyzed - total_flagged

    prompt = f"""You are a content moderation analyst. Summarize the following moderation results:

Total analyzed: {total_analyzed}
Total flagged: {total_flagged}
Total allowed: {total_allowed}

Category breakdown: {category_counts}

Top violations: {top_violations}

Provide a concise 3-5 sentence summary of the moderation outcomes, highlighting the most common violation categories and overall content safety posture."""

    messages = [
        {
            "role": "system",
            "content": "You are a content safety analyst providing moderation summaries.",
        },
        {"role": "user", "content": prompt},
    ]

    response = call_chat(
        messages, model=model or OPENAI_CHAT_MODEL, temperature=0.0, max_tokens=512
    )
    summary_text = response.choices[0].message.content.strip()

    return ModerationSummary(
        total_analyzed=total_analyzed,
        total_flagged=total_flagged,
        total_allowed=total_allowed,
        category_breakdown=category_counts,
        top_violations=top_violations,
        summary_text=summary_text,
    )


def generate_moderation_report(decisions, model=None):
    summary = summarize_moderation_decisions(
        decisions, model=model or OPENAI_CHAT_MODEL
    )
    report = {
        "summary_text": summary.summary_text,
        "total_analyzed": summary.total_analyzed,
        "flagged_percentage": round(
            summary.total_flagged / max(summary.total_analyzed, 1) * 100, 2
        ),
        "category_breakdown": summary.category_breakdown,
        "top_violations": summary.top_violations,
    }
    return report
