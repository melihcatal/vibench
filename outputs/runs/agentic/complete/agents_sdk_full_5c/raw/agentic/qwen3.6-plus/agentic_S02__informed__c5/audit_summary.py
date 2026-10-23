"""Summarize federated-login audit events using OpenAI GPT-4.

This module sends federated login audit events to the OpenAI Chat Completions API
and generates a human-readable summary of login activity patterns.

Provider: OpenAI / Azure OpenAI chat completions
SDK: openai
Auth env vars: OPENAI_API_KEY
Model: gpt-4
"""

import os
import json
from typing import List, Dict, Any, Optional

from openai import OpenAI

from identity_models import AuditEvent


def summarize_audit_events(
    audit_events: List[AuditEvent],
    model: str = "gpt-4",
    max_tokens: int = 500,
    temperature: float = 0.3,
) -> str:
    """Generate a summary of federated-login audit events using OpenAI GPT-4.

    Args:
        audit_events: List of AuditEvent objects to summarize.
        model: OpenAI model identifier (default: gpt-4).
        max_tokens: Maximum tokens in the response.
        temperature: Sampling temperature for generation.

    Returns:
        Human-readable summary string of the audit events.

    Raises:
        ValueError: If no events provided or OPENAI_API_KEY is missing.
        openai.OpenAIError: If the API request fails.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    if not audit_events:
        raise ValueError("No audit events provided")

    events_data = []
    for event in audit_events:
        events_data.append({
            "event_id": event.event_id,
            "event_type": event.event_type,
            "timestamp": event.timestamp,
            "user_subject": event.user_subject,
            "client_id": event.client_id,
            "connection": event.connection,
            "success": event.success,
            "error_description": event.error_description,
        })

    events_json = json.dumps(events_data, indent=2)

    client = OpenAI(api_key=api_key)

    system_prompt = (
        "You are a security analyst summarizing federated login audit events "
        "from an OAuth/OIDC identity provider. Analyze the events and provide "
        "a concise summary highlighting: total events, success/failure rates, "
        "unique users, connections used, and any notable patterns or anomalies."
    )

    user_prompt = (
        f"Summarize the following federated login audit events:\n\n{events_json}"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        max_tokens=max_tokens,
        temperature=temperature,
    )

    summary = response.choices[0].message.content
    return summary or "No summary generated."


def summarize_audit_events_with_context(
    audit_events: List[AuditEvent],
    additional_context: Optional[str] = None,
) -> str:
    """Summarize audit events with additional operational context.

    Args:
        audit_events: List of AuditEvent objects.
        additional_context: Extra context for the summary.

    Returns:
        Summary string with contextual analysis.
    """
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is not set")

    events_data = [event.to_dict() for event in audit_events]
    events_json = json.dumps(events_data, indent=2)

    client = OpenAI(api_key=api_key)

    context_section = ""
    if additional_context:
        context_section = f"\nAdditional context: {additional_context}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a security operations analyst. Summarize OAuth/OIDC "
                    "federated login audit events and identify any security concerns."
                ),
            },
            {
                "role": "user",
                "content": (
                    f"Audit events:\n{events_json}{context_section}\n\n"
                    "Provide a summary with security observations."
                ),
            },
        ],
        max_tokens=600,
        temperature=0.2,
    )

    return response.choices[0].message.content or "No summary generated."


if __name__ == "__main__":
    events = [
        AuditEvent(
            event_id="evt_001",
            event_type="federated_login",
            timestamp="2024-01-15T10:30:00Z",
            user_subject="auth0|user123",
            client_id="abc123",
            connection="google-oauth2",
            success=True,
        ),
    ]
    summary = summarize_audit_events(events)
    print(summary)
