"""
moderation_summary.py - Summarize moderation decisions.

Provider: OpenAI Chat Completions API (GPT-4o-mini)
  - SDK: openai
  - Env: OPENAI_API_KEY
  - Model: gpt-4o-mini
  - API: api.openai.com
"""

from __future__ import annotations

import json
import os
from typing import Optional, List, Dict, Any

from openai import OpenAI

from safety_models import BatchModerationResponse


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required.")
    return OpenAI(api_key=api_key)


def summarize_moderation_decisions(
    batch_response: BatchModerationResponse,
    max_summary_length: int = 500,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Generate a natural language summary of batch moderation decisions using GPT-4o-mini.

    Args:
        batch_response: The batch moderation response to summarize.
        max_summary_length: Maximum length of the summary in characters.
        client: Optional pre-configured OpenAI client.

    Returns:
        A natural language summary of the moderation results.
    """
    if client is None:
        client = get_openai_client()

    summary_data = _build_summary_context(batch_response)

    prompt = (
        f"You are a content moderation analyst. Based on the following moderation data, "
        f"write a concise summary (under {max_summary_length} characters) of the content "
        f"safety review results.\n\n"
        f"Moderation Data:\n{json.dumps(summary_data, indent=2)}\n\n"
        f"Summary:"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You summarize content moderation decisions. "
                    "Provide clear, actionable insights about the safety profile of the reviewed content."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=300,
        temperature=0.3,
    )

    summary = response.choices[0].message.content.strip()
    return summary


def summarize_moderation_reason(
    moderation_response: Any,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Generate a brief rationale explaining why specific content was flagged.

    Args:
        moderation_response: A ModerationResponse or dict with moderation data.
        client: Optional pre-configured OpenAI client.

    Returns:
        A brief explanation of the moderation decision.
    """
    if client is None:
        client = get_openai_client()

    if hasattr(moderation_response, "to_dict"):
        data = moderation_response.to_dict()
    elif hasattr(moderation_response, "__dict__"):
        data = moderation_response.__dict__
    else:
        data = dict(moderation_response)

    prompt = (
        f"Based on these moderation results, explain why the content was flagged:\n"
        f"{json.dumps(data, indent=2, default=str)}\n\n"
        f"Explanation:"
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You explain content moderation decisions in clear, professional language. "
                    "Focus on which policy categories were violated and the severity."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=200,
        temperature=0.2,
    )

    return response.choices[0].message.content.strip()


def generate_reviewer_report(
    batch_response: BatchModerationResponse,
    include_recommendations: bool = True,
    client: Optional[OpenAI] = None,
) -> str:
    """
    Generate a structured report for human reviewers using GPT-4o-mini.

    Args:
        batch_response: The batch moderation response.
        include_recommendations: Whether to include action recommendations.
        client: Optional pre-configured OpenAI client.

    Returns:
        A formatted reviewer report.
    """
    if client is None:
        client = get_openai_client()

    summary_data = _build_summary_context(batch_response)
    recommendation_clause = (
        "Include specific recommendations for next steps." if include_recommendations
        else "Do not include recommendations."
    )

    prompt = (
        f"Generate a structured content moderation review report based on this data:\n"
        f"{json.dumps(summary_data, indent=2)}\n\n"
        f"{recommendation_clause}\n"
        f"Format the report with clear sections: Overview, Findings, Details, and Recommendations."
    )

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior content moderation analyst preparing reports for human reviewers. "
                    "Use professional, structured formatting."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        max_tokens=600,
        temperature=0.3,
    )

    return response.choices[0].message.content.strip()


def _build_summary_context(batch_response: BatchModerationResponse) -> Dict[str, Any]:
    """Build a JSON-serializable context from batch moderation results."""
    results = []
    for r in batch_response.results:
        entry = {
            "text_preview": r.text[:100] + "..." if len(r.text) > 100 else r.text,
            "overall_safe": r.overall_safe,
            "blocklist_match": r.blocklist_match,
            "categories": [],
        }
        for cat in r.categories:
            entry["categories"].append({
                "category": cat.category,
                "severity": cat.severity,
                "label": cat.label,
            })
        results.append(entry)

    return {
        "total_items": batch_response.total_items,
        "safe_count": batch_response.total_items - batch_response.unsafe_count,
        "unsafe_count": batch_response.unsafe_count,
        "results": results,
    }
