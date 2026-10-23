"""
audit_summary.py - Summarize federated-login audit events
Provider: OpenAI (openai.com) - GPT-4 model for audit event summarization
"""

import os
import json
from typing import List, Dict, Any, Optional
from datetime import datetime

from openai import OpenAI


OPENAI_MODEL = "gpt-4"


def build_audit_summary_prompt(
    audit_events: List[Dict[str, Any]],
    time_window: str = "last 24 hours",
) -> str:
    """Build a prompt for OpenAI GPT-4 to summarize federated-login audit events."""
    events_json = json.dumps(audit_events, indent=2, default=str)

    prompt = (
        f"You are a security analyst reviewing federated login audit events "
        f"from an Auth0 identity provider over the {time_window}.\n\n"
        f"Audit events:\n{events_json}\n\n"
        f"Please provide a concise summary that includes:\n"
        f"1. Total number of login attempts and success rate\n"
        f"2. Any failed login patterns or anomalies\n"
        f"3. Identity providers or connections used\n"
        f"4. Geographic distribution if available\n"
        f"5. Recommendations for security improvements\n\n"
        f"Keep the summary under 300 words and use bullet points."
    )
    return prompt


def summarize_audit_events(
    audit_events: List[Dict[str, Any]],
    time_window: str = "last 24 hours",
    model: str = OPENAI_MODEL,
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Summarize federated-login audit events using OpenAI GPT-4.

    Provider: OpenAI (openai.com)
    Model: gpt-4
    """
    effective_api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not effective_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    prompt = build_audit_summary_prompt(audit_events, time_window)

    client = OpenAI(api_key=effective_api_key)

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a security analyst specializing in identity and access management. "
                    "Analyze federated login audit data and provide actionable security insights."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1500,
    )

    summary_text = response.choices[0].message.content.strip()

    return {
        "success": True,
        "summary": summary_text,
        "model": model,
        "provider": "openai",
        "event_count": len(audit_events),
        "time_window": time_window,
        "generated_at": datetime.utcnow().isoformat(),
    }


def generate_risk_report(
    audit_events: List[Dict[str, Any]],
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Generate a risk assessment report from audit events using OpenAI GPT-4.

    Provider: OpenAI
    Model: gpt-4
    """
    effective_api_key = api_key or os.environ.get("OPENAI_API_KEY", "")
    if not effective_api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    events_json = json.dumps(audit_events, indent=2, default=str)

    prompt = (
        f"Analyze these federated login audit events and produce a risk assessment.\n\n"
        f"Events:\n{events_json}\n\n"
        f"Provide:\n"
        f"- Overall risk level (LOW/MEDIUM/HIGH/CRITICAL)\n"
        f"- Top 3 risks identified\n"
        f"- Immediate actions recommended\n"
        f"- Long-term recommendations"
    )

    client = OpenAI(api_key=effective_api_key)

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a senior IAM security analyst. Provide risk assessments "
                    "for federated authentication systems. Be specific and actionable."
                ),
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.2,
        max_tokens=2000,
    )

    report_text = response.choices[0].message.content.strip()

    return {
        "success": True,
        "report": report_text,
        "model": "gpt-4",
        "provider": "openai",
        "generated_at": datetime.utcnow().isoformat(),
    }
