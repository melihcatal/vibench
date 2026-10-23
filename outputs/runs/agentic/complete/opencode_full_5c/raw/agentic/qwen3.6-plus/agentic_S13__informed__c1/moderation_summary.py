import os
from typing import Optional

import anthropic

from safety_models import ModerationResponse, response_to_dict

ANTHROPIC_API_KEY = os.environ.get("ANTHROPIC_API_KEY", "")
CLAUDE_MODEL = "claude-3-5-sonnet-20241022"


def _build_summary_prompt(moderation_results: list[dict]) -> str:
    lines = [
        "Summarize the following moderation decisions in a concise report.",
        "Include: total items reviewed, number flagged/blocked, top violation categories, and recommended actions.",
        "",
    ]
    for i, result in enumerate(moderation_results, 1):
        lines.append(f"Item {i}:")
        lines.append(f"  Text: {result.get('text', '')[:200]}")
        lines.append(f"  Decision: {result.get('decision', 'unknown')}")
        cats = result.get("flagged_categories", [])
        if cats:
            lines.append(f"  Flagged categories: {', '.join(cats)}")
        scores = result.get("category_scores", [])
        for s in scores:
            lines.append(f"  {s['category']}: {s['score']} ({s['severity']})")
        lines.append("")
    return "\n".join(lines)


def generate_moderation_summary(
    moderation_results: list[dict],
    max_tokens: int = 1024,
) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt = _build_summary_prompt(moderation_results)

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=max_tokens,
        system="You are a content moderation analyst. Provide clear, structured summaries of moderation decisions.",
        messages=[
            {"role": "user", "content": prompt},
        ],
    )

    summary_text = message.content[0].text

    flagged = sum(1 for r in moderation_results if r.get("decision") != "allow")
    blocked = sum(1 for r in moderation_results if r.get("decision") == "block")

    return {
        "summary": summary_text,
        "total_reviewed": len(moderation_results),
        "flagged_count": flagged,
        "blocked_count": blocked,
        "model": CLAUDE_MODEL,
        "provider": "anthropic",
    }


def generate_case_summary(
    case_id: str,
    moderation_result: dict,
    reviewer_notes: Optional[str] = None,
) -> dict:
    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    prompt_parts = [
        f"Generate a concise case summary for moderation case {case_id}.",
        f"Decision: {moderation_result.get('decision', 'unknown')}",
        f"Content: {moderation_result.get('text', '')[:300]}",
    ]
    if moderation_result.get("flagged_categories"):
        prompt_parts.append(
            f"Violations: {', '.join(moderation_result['flagged_categories'])}"
        )
    if reviewer_notes:
        prompt_parts.append(f"Reviewer notes: {reviewer_notes}")
    prompt_parts.append(
        "Format: 2-3 sentences covering the violation type, severity, and recommended action."
    )

    message = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=512,
        system="You are a moderation case summarization assistant.",
        messages=[
            {"role": "user", "content": "\n".join(prompt_parts)},
        ],
    )

    return {
        "case_id": case_id,
        "summary": message.content[0].text,
        "model": CLAUDE_MODEL,
        "provider": "anthropic",
    }
