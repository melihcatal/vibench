"""
audit_summary.py - Summarize federated-login audit events using
an LLM to generate human-readable summaries and anomaly reports.

Provider: OpenAI Chat Completions API
SDK: openai
Auth env vars: OPENAI_API_KEY
Model: gpt-4o
"""

import json
import os
from typing import Optional

from openai import OpenAI


def get_openai_client() -> OpenAI:
    """Create an OpenAI client using the OPENAI_API_KEY environment variable."""
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable must be set")
    return OpenAI(api_key=api_key)


def summarize_audit_events(
    audit_events: list[dict],
    summary_type: str = "overview",
    max_tokens: int = 1024,
) -> str:
    """
    Generate a summary of federated-login audit events using OpenAI gpt-4o.

    Args:
        audit_events: List of audit event dicts with keys like
            event_type, user_id, provider, timestamp, error_message, etc.
        summary_type: Type of summary ('overview', 'errors', 'anomalies')
        max_tokens: Maximum tokens for the response

    Returns:
        Human-readable summary text.
    """
    client = get_openai_client()

    events_json = json.dumps(audit_events, indent=2, default=str)

    prompt_map = {
        "overview": (
            "Summarize the following federated-login audit events. "
            "Include: total event count, breakdown by event type, "
            "unique users, identity providers used, and time range. "
            "Keep the summary concise and structured."
        ),
        "errors": (
            "Analyze the following federated-login audit events and summarize "
            "all error conditions. Group errors by type, identify affected users, "
            "and suggest potential root causes."
        ),
        "anomalies": (
            "Review the following federated-login audit events and identify "
            "any anomalous patterns: unusual login times, repeated failures, "
            "multiple providers for the same user, or suspicious state changes. "
            "Flag anything that warrants investigation."
        ),
    }

    instruction = prompt_map.get(summary_type, prompt_map["overview"])

    messages = [
        {
            "role": "system",
            "content": (
                "You are a security analyst specializing in identity and access management. "
                "Provide clear, actionable summaries of federated-login audit data."
            ),
        },
        {
            "role": "user",
            "content": f"{instruction}\n\nAudit Events:\n{events_json}",
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=max_tokens,
        temperature=0.3,
    )

    return response.choices[0].message.content


def generate_audit_report(
    audit_events: list[dict],
    report_format: str = "markdown",
) -> str:
    """
    Generate a comprehensive audit report for federated login events
    using OpenAI gpt-4o.

    Returns the report in the requested format.
    """
    client = get_openai_client()

    events_json = json.dumps(audit_events, indent=2, default=str)

    messages = [
        {
            "role": "system",
            "content": (
                "You are an identity security analyst. Generate structured audit reports "
                "for federated authentication systems. Output in the requested format."
            ),
        },
        {
            "role": "user",
            "content": (
                f"Generate a {report_format}-formatted audit report for these "
                f"federated-login events:\n\n{events_json}\n\n"
                "Include: Executive Summary, Event Breakdown, Error Analysis, "
                "Recommendations, and Risk Assessment."
            ),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=2048,
        temperature=0.2,
    )

    return response.choices[0].message.content


def detect_login_anomalies(audit_events: list[dict]) -> list[dict]:
    """
    Use OpenAI gpt-4o to detect anomalous patterns in federated login events.

    Returns a list of detected anomalies with descriptions and severity levels.
    """
    client = get_openai_client()

    events_json = json.dumps(audit_events, indent=2, default=str)

    messages = [
        {
            "role": "system",
            "content": (
                "You are a security analyst. Analyze login audit data and return "
                "a JSON array of anomalies. Each anomaly should have: 'type', "
                "'description', 'severity' (low/medium/high/critical), and "
                "'affected_event_ids'."
            ),
        },
        {
            "role": "user",
            "content": (
                "Analyze these federated-login audit events for anomalies:\n\n"
                f"{events_json}\n\nReturn ONLY a valid JSON array of anomalies."
            ),
        },
    ]

    response = client.chat.completions.create(
        model="gpt-4o",
        messages=messages,
        max_tokens=1024,
        temperature=0.1,
        response_format={"type": "json_object"},
    )

    result_text = response.choices[0].message.content
    try:
        result = json.loads(result_text)
        return result.get("anomalies", result) if isinstance(result, dict) else result
    except json.JSONDecodeError:
        return [{"type": "parse_error", "description": "Could not parse LLM response"}]
