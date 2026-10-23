"""
moderation_summary.py - Summarize moderation decisions.

Uses the OpenAI Chat Completions API (api.openai.com) with gpt-4o-mini to generate
human-readable summaries of moderation decision batches for review and reporting.
"""

import os
import json
from datetime import datetime

import openai


SUMMARY_MODEL = "gpt-4o-mini"


def _get_openai_client():
    """Create an OpenAI client for chat completions."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")
    client = openai.OpenAI(api_key=api_key)
    return client


def generate_moderation_summary(
    moderation_results: list[dict],
    summary_type: str = "overview",
) -> dict:
    """
    Generate a human-readable summary of moderation decisions.

    Args:
        moderation_results: List of moderation result dicts from moderate_batch.py.
        summary_type: Type of summary to generate ('overview', 'detailed', 'category_breakdown').

    Returns:
        Dictionary with:
            - summary_text: Human-readable summary
            - statistics: Numeric breakdown
            - model: model used for generation
            - provider: openai
    """
    client = _get_openai_client()

    total = len(moderation_results)
    flagged = sum(1 for r in moderation_results if r.get("flagged", False))
    safe = total - flagged

    category_counts = {}
    for result in moderation_results:
        for cat in result.get("flagged_categories", []):
            category_counts[cat] = category_counts.get(cat, 0) + 1

    stats = {
        "total_messages": total,
        "flagged_count": flagged,
        "safe_count": safe,
        "flag_rate": round(flagged / total, 4) if total > 0 else 0.0,
        "category_counts": category_counts,
    }

    summary_prompt = _build_summary_prompt(stats, moderation_results, summary_type)

    response = client.chat.completions.create(
        model=SUMMARY_MODEL,
        messages=[
            {"role": "system", "content": "You are a content moderation analyst. Provide clear, concise summaries of moderation decisions for review teams."},
            {"role": "user", "content": summary_prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary_text = response.choices[0].message.content.strip()

    return {
        "summary_text": summary_text,
        "statistics": stats,
        "summary_type": summary_type,
        "generated_at": datetime.utcnow().isoformat(),
        "model": SUMMARY_MODEL,
        "provider": "openai",
        "provider_endpoint": "api.openai.com/v1/chat/completions",
    }


def _build_summary_prompt(stats: dict, results: list[dict], summary_type: str) -> str:
    """Build the prompt for summary generation."""
    if summary_type == "overview":
        prompt = f"""Provide a brief overview of these moderation results:
- Total messages processed: {stats['total_messages']}
- Flagged messages: {stats['flagged_count']} ({stats['flag_rate']*100:.1f}%)
- Safe messages: {stats['safe_count']}
- Top violation categories: {json.dumps(stats['category_counts'])}

Summarize the overall content safety posture and any notable patterns."""

    elif summary_type == "detailed":
        flagged_results = [r for r in results if r.get("flagged")]
        sample_flagged = flagged_results[:5]
        prompt = f"""Provide a detailed analysis of these moderation decisions:

Statistics:
- Total: {stats['total_messages']}, Flagged: {stats['flagged_count']}, Safe: {stats['safe_count']}
- Flag rate: {stats['flag_rate']*100:.1f}%

Sample flagged messages (first {len(sample_flagged)}):
{json.dumps(sample_flagged, indent=2)}

Category breakdown:
{json.dumps(stats['category_counts'], indent=2)}

Analyze the patterns, severity distribution, and provide recommendations for the moderation team."""

    elif summary_type == "category_breakdown":
        prompt = f"""Provide a category-focused breakdown of these moderation results:

Category violation counts:
{json.dumps(stats['category_counts'], indent=2)}

Total messages: {stats['total_messages']}
Overall flag rate: {stats['flag_rate']*100:.1f}%

For each category that has violations, explain what types of content typically trigger it
and suggest appropriate review actions."""
    else:
        prompt = f"Summarize these moderation results: {json.dumps(stats)}"

    return prompt


def generate_daily_summary(
    daily_results: list[dict],
    date_str: str = None,
) -> dict:
    """
    Generate a daily moderation summary report.

    Args:
        daily_results: List of all moderation results for the day.
        date_str: Date string for the report (defaults to today).

    Returns:
        Daily summary report dict.
    """
    if date_str is None:
        date_str = datetime.utcnow().strftime("%Y-%m-%d")

    summary = generate_moderation_summary(daily_results, summary_type="detailed")

    return {
        "report_date": date_str,
        "summary": summary,
        "report_type": "daily_moderation_summary",
        "provider": "openai",
    }


if __name__ == "__main__":
    sample_results = [
        {"flagged": False, "flagged_categories": []},
        {"flagged": True, "flagged_categories": ["harassment"]},
        {"flagged": True, "flagged_categories": ["violence", "harassment/threatening"]},
        {"flagged": False, "flagged_categories": []},
        {"flagged": True, "flagged_categories": ["hate"]},
    ]
    summary = generate_moderation_summary(sample_results, summary_type="overview")
    print(summary["summary_text"])
