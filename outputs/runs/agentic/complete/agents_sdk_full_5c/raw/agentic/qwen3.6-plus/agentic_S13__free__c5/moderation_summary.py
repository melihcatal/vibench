"""
[LATER-STEP] moderation_summary.py
Summarize moderation decisions across a set of texts using OpenAI GPT-4o.
Provider: OpenAI — model identifier: gpt-4o
API hostname: api.openai.com
"""

from typing import Optional, Dict, Any, List
import json

from safety_client import get_openai_client, load_safety_config
from safety_models import ModerationResult, ModerationSummary, ModerationDecision


DEFAULT_MODEL = "gpt-4o"


def build_summary_prompt(results: List[Dict[str, Any]]) -> str:
    """Build a prompt for the moderation summary generation."""
    prompt_parts = [
        "You are a moderation analyst. Given the following moderation results, produce a structured summary.",
        "",
        "Provide the following information in JSON format:",
        "- total_texts: total number of texts reviewed",
        "- allowed: count of allowed texts",
        "- flagged: count of flagged texts",
        "- blocked: count of blocked texts",
        "- under_review: count of texts marked for review",
        "- category_counts: dict mapping each category name to how many times it was triggered",
        "- average_scores: dict mapping each category name to the average score across all texts",
        "- top_risk_text: the single text with the highest risk score",
        "- top_risk_category: the category with the highest score for that text",
        "- top_risk_score: the highest score value",
        "",
        "Here are the results:",
        json.dumps(results, indent=2),
    ]
    return "\n".join(prompt_parts)


def moderation_summary(
    moderation_results: List[ModerationResult],
    model: str = DEFAULT_MODEL,
    config: Optional[Dict[str, Any]] = None,
) -> ModerationSummary:
    """
    Summarize moderation decisions using OpenAI's gpt-4o model.
    Accepts a list of ModerationResult objects and returns a ModerationSummary.
    """
    if config is None:
        config = load_safety_config()

    client = get_openai_client(config)

    result_dicts = [r.to_dict() for r in moderation_results]
    prompt = build_summary_prompt(result_dicts)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": "You are a JSON-only response assistant for moderation analysis."},
            {"role": "user", "content": prompt},
        ],
        temperature=0.0,
        response_format={"type": "json_object"},
    )

    content = response.choices[0].message.content
    try:
        summary_data = json.loads(content)
    except json.JSONDecodeError:
        summary_data = {}

    return ModerationSummary(
        total_texts=summary_data.get("total_texts", len(moderation_results)),
        allowed=summary_data.get("allowed", 0),
        flagged=summary_data.get("flagged", 0),
        blocked=summary_data.get("blocked", 0),
        under_review=summary_data.get("under_review", 0),
        category_counts=summary_data.get("category_counts", {}),
        average_scores=summary_data.get("average_scores", {}),
        top_risk_text=summary_data.get("top_risk_text"),
        top_risk_category=summary_data.get("top_risk_category"),
        top_risk_score=summary_data.get("top_risk_score", 0.0),
    )


def moderation_summary_dict(
    moderation_results: List[ModerationResult],
    model: str = DEFAULT_MODEL,
    config: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    """Summarize moderation decisions and return as a dict."""
    result = moderation_summary(moderation_results, model=model, config=config)
    return result.to_dict()


if __name__ == "__main__":
    from safety_models import CategoryScore
    sample_results = [
        ModerationResult(
            text="Hello there",
            flagged=False,
            decision=ModerationDecision.ALLOW,
            categories=[CategoryScore(category="hate", score=0.01)],
            highest_score=0.01,
        ),
        ModerationResult(
            text="Violent threat here",
            flagged=True,
            decision=ModerationDecision.BLOCK,
            categories=[CategoryScore(category="violence", score=0.95)],
            highest_category="violence",
            highest_score=0.95,
        ),
    ]
    summary = moderation_summary_dict(sample_results)
    print(summary)
