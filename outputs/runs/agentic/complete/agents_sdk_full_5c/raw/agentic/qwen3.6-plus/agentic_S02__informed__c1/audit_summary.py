"""
[LATER-STEP] Summarize federated-login audit events using OpenAI GPT chat completions.

Uses the OpenAI Chat Completions API (sdk=openai, model=gpt-4o) to analyze
and summarize federated login audit events, identifying patterns, anomalies,
and providing actionable insights.

Required env vars: OPENAI_API_KEY
"""

import json
import logging
from typing import Any, Dict, List, Optional

from openai import OpenAI

from identity_client import get_audit_logger
from identity_models import AuditEvent

logger = logging.getLogger(__name__)

# OpenAI GPT model family identifier
AUDIT_SUMMARY_MODEL = "gpt-4o"


def format_audit_events(events: List[AuditEvent]) -> str:
    """Format audit events into a readable text summary for the LLM."""
    lines = []
    lines.append(f"Total audit events: {len(events)}")
    lines.append("")

    # Group by event type
    by_type: Dict[str, List[AuditEvent]] = {}
    for event in events:
        by_type.setdefault(event.event_type, []).append(event)

    for event_type, type_events in by_type.items():
        lines.append(f"--- {event_type} ({len(type_events)} events) ---")
        for evt in type_events[:5]:  # Show up to 5 per type
            lines.append(
                f"  [{evt.timestamp}] sub={evt.sub} provider={evt.provider} "
                f"email={evt.email} state={evt.state}"
            )
            if evt.details:
                lines.append(f"    details: {json.dumps(evt.details)}")
        if len(type_events) > 5:
            lines.append(f"  ... and {len(type_events) - 5} more events")
        lines.append("")

    return "\n".join(lines)


def summarize_audit_events(
    events: Optional[List[AuditEvent]] = None,
    api_key: Optional[str] = None,
    model: str = AUDIT_SUMMARY_MODEL,
    max_tokens: int = 2048,
) -> str:
    """
    Summarize federated-login audit events using OpenAI GPT-4o.

    Uses the OpenAI Chat Completions API:
        POST https://api.openai.com/v1/chat/completions

    Required env var: OPENAI_API_KEY
    """
    if events is None:
        audit_logger = get_audit_logger()
        events = audit_logger.get_events()

    if not events:
        return "No audit events to summarize."

    event_text = format_audit_events(events)

    system_prompt = (
        "You are a security analyst specializing in identity and access management. "
        "Analyze the following federated login audit events and provide a concise summary. "
        "Include: (1) overall login activity patterns, (2) any anomalies or security concerns, "
        "(3) provider distribution, (4) success vs failure rates, and (5) actionable recommendations. "
        "Be specific and data-driven."
    )

    client = OpenAI(api_key=api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": event_text},
        ],
        max_tokens=max_tokens,
        temperature=0.3,
    )

    summary = response.choices[0].message.content or ""

    logger.info(
        "Generated audit summary using OpenAI %s (usage: %s tokens)",
        model,
        response.usage.total_tokens if response.usage else "unknown",
    )

    return summary


def generate_audit_report(
    events: Optional[List[AuditEvent]] = None,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a full audit report with summary and metadata.
    """
    if events is None:
        audit_logger = get_audit_logger()
        events = audit_logger.get_events()

    summary = summarize_audit_events(events, api_key=api_key)

    # Quick stats
    event_counts: Dict[str, int] = {}
    provider_counts: Dict[str, int] = {}
    for evt in events:
        event_counts[evt.event_type] = event_counts.get(evt.event_type, 0) + 1
        provider_counts[evt.provider] = provider_counts.get(evt.provider, 0) + 1

    return {
        "summary": summary,
        "total_events": len(events),
        "event_type_counts": event_counts,
        "provider_counts": provider_counts,
        "model_used": AUDIT_SUMMARY_MODEL,
        "provider": "openai",
    }
