"""Summarize federated-login audit events using OpenAI chat completions."""

import os
import json
from typing import Optional, List, Dict, Any

from openai import OpenAI

from identity_models import AuditEvent


def build_audit_prompt(events: List[Dict[str, Any]], focus: Optional[str] = None) -> str:
    """Build a prompt for summarizing federated-login audit events."""
    events_json = json.dumps(events, indent=2)
    prompt = (
        "You are a security analyst reviewing federated-login audit events from Google Identity Platform.\n\n"
        "Below are the audit events:\n\n"
        f"{events_json}\n\n"
    )
    if focus:
        prompt += f"Focus your summary on: {focus}\n\n"
    prompt += (
        "Provide a concise summary that includes:\n"
        "- Total number of login attempts\n"
        "- Success rate\n"
        "- Notable patterns (failed logins, unusual IPs, etc.)\n"
        "- Any security recommendations\n"
    )
    return prompt


def summarize_audit_events(
    events: List[Dict[str, Any]],
    focus: Optional[str] = None,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize federated-login audit events using OpenAI's chat completions API.
    """
    client = OpenAI(
        api_key=api_key or os.environ.get("OPENAI_API_KEY", ""),
    )

    prompt = build_audit_prompt(events, focus)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a security analyst specializing in federated identity and OAuth/OIDC audit log analysis.",
            },
            {
                "role": "user",
                "content": prompt,
            },
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    summary_text = response.choices[0].message.content if response.choices else ""

    return {
        "summary": summary_text,
        "model": model,
        "provider": "OpenAI",
        "event_count": len(events),
        "focus": focus,
        "usage": {
            "prompt_tokens": response.usage.prompt_tokens if response.usage else None,
            "completion_tokens": response.usage.completion_tokens if response.usage else None,
            "total_tokens": response.usage.total_tokens if response.usage else None,
        } if response.usage else {},
    }


def summarize_events_from_models(
    audit_events: List[AuditEvent],
    focus: Optional[str] = None,
    model: str = "gpt-4o-mini",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """Summarize a list of AuditEvent model instances using OpenAI."""
    events_data = [e.to_document() for e in audit_events]
    return summarize_audit_events(events_data, focus=focus, model=model, api_key=api_key)


if __name__ == "__main__":
    sample_events = [
        {
            "event_type": "login_attempt",
            "timestamp": 1700000000.0,
            "user_sub": "user123",
            "client_id": "abc123",
            "provider": "Google Identity Platform",
            "ip_address": "192.168.1.1",
            "success": True,
        },
        {
            "event_type": "login_attempt",
            "timestamp": 1700000100.0,
            "user_sub": "user456",
            "client_id": "abc123",
            "provider": "Google Identity Platform",
            "ip_address": "10.0.0.5",
            "success": False,
            "details": {"error": "invalid_code"},
        },
    ]
    result = summarize_audit_events(sample_events)
    print(result["summary"])
