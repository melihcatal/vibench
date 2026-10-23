"""
[LATER-STEP] moderation_summary.py - Summarize moderation decisions.

Uses the OpenAI Chat Completions API (model: gpt-4o) to generate concise
human-readable summaries of moderation outcomes, flagging rationale,
and recommended reviewer actions.
"""

from __future__ import annotations

import json
from typing import Any, Dict, List, Optional

from openai import OpenAI

from safety_client import SafetyClient
from safety_models import ModerationResult


_MODERATION_SUMMARY_PROMPT = """\
You are a content moderation summarization assistant. Given moderation results
from the OpenAI omni-moderation-latest model, produce a concise, structured
summary for a human reviewer.

Format your response as JSON with the following keys:
- overall_verdict: one of "safe", "review_needed", "remove_immediately"
- risk_level: a number from 1 (low) to 5 (critical)
- summary: a 1-2 sentence plain-text summary
- key_concerns: a list of up to 3 specific concern strings
- recommended_action: a short recommended action string

Input moderation data:
{moderation_data}
"""


def summarize_moderation(
    moderation_results: List[ModerationResult],
    api_key: Optional[str] = None,
    model: str = "gpt-4o",
) -> Dict[str, Any]:
    """
    Generate a structured summary of a list of moderation results.

    Parameters
    ----------
    moderation_results : list[ModerationResult]
        The results from prior moderation calls.
    api_key : str, optional
        OpenAI API key. Falls back to OPENAI_API_KEY env var.
    model : str
        OpenAI model to use for summarization (default: gpt-4o).

    Returns
    -------
    dict
        The structured JSON summary as a dict.
    """
    data_dump = json.dumps(
        [
            {
                "text_preview": r.text[:200],
                "flagged": r.flagged,
                "severity": r.severity.value,
                "category_scores": [
                    {"category": cs.category, "score": cs.score, "flagged": cs.flagged}
                    for cs in r.category_scores
                ],
            }
            for r in moderation_results
        ],
        indent=2,
    )
    prompt = _MODERATION_SUMMARY_PROMPT.format(moderation_data=data_dump)

    api_key = api_key or __import__("os").environ.get("OPENAI_API_KEY", "")
    client = OpenAI(api_key=api_key)

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are a content moderation summarizer. "
                        "Always respond with valid JSON only."
                    ),
                },
                {"role": "user", "content": prompt},
            ],
            temperature=0.2,
            max_tokens=500,
        )
        content = response.choices[0].message.content or "{}"
        return json.loads(content)
    finally:
        if hasattr(client, "close"):
            client.close()


def format_summary_text(summary: Dict[str, Any]) -> str:
    """Format a summary dict into a readable string."""
    lines = [
        f"Overall Verdict: {summary.get('overall_verdict', 'unknown')}",
        f"Risk Level: {summary.get('risk_level', 'N/A')}/5",
        f"Summary: {summary.get('summary', '')}",
        "",
        "Key Concerns:",
    ]
    for concern in summary.get("key_concerns", []):
        lines.append(f"  - {concern}")
    lines.append(f"\nRecommended Action: {summary.get('recommended_action', '')}")
    return "\n".join(lines)


def main() -> None:
    import sys
    if len(sys.argv) < 2:
        print("Usage: python moderation_summary.py <text1> [<text2> ...]")
        sys.exit(1)
    texts = sys.argv[1:]
    client = SafetyClient()
    results = [client.moderate_single(t) for t in texts]
    client.close()
    summary = summarize_moderation(results)
    print(format_summary_text(summary))


if __name__ == "__main__":
    main()
