import os
import json
import time
from typing import Dict, Any, List, Optional

from openai import OpenAI

from identity_models import AuditEvent


OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-4o-mini"


def summarize_audit_events(
    audit_events: List[Dict[str, Any]],
    summary_type: str = "overview",
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if not api_key:
        api_key = OPENAI_API_KEY

    client = OpenAI(api_key=api_key)

    events_json = json.dumps(audit_events, indent=2)

    prompt_instructions = {
        "overview": "Provide a high-level summary of these federated login audit events, including total count, success rate, and most common event types.",
        "security": "Analyze these federated login audit events for potential security concerns, failed authentication patterns, or suspicious activity.",
        "performance": "Summarize the performance characteristics of these federated login events, including timing patterns and error rates.",
        "compliance": "Review these federated login audit events for compliance-relevant information, noting any gaps or concerns.",
    }

    instruction = prompt_instructions.get(summary_type, prompt_instructions["overview"])

    system_prompt = (
        "You are a security analyst reviewing federated login audit events. "
        "Analyze the provided JSON audit event data and provide a concise, structured summary. "
        "Focus on patterns, anomalies, and actionable insights."
    )

    user_prompt = f"{instruction}\n\nAudit Events:\n{events_json}"

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )

    summary_text = response.choices[0].message.content

    return {
        "summary": summary_text,
        "summary_type": summary_type,
        "event_count": len(audit_events),
        "model": OPENAI_MODEL,
        "provider": "openai",
        "generated_at": time.time(),
    }


def generate_audit_insights(
    audit_events: List[Dict[str, Any]],
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if not api_key:
        api_key = OPENAI_API_KEY

    client = OpenAI(api_key=api_key)

    events_json = json.dumps(audit_events, indent=2)

    system_prompt = (
        "You are an identity and access management expert. "
        "Analyze federated login audit events and provide structured insights in JSON format. "
        "Return a JSON object with keys: success_rate, top_providers, error_patterns, recommendations."
    )

    user_prompt = f"Analyze these federated login audit events and return structured insights as JSON:\n\n{events_json}"

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=1024,
        response_format={"type": "json_object"},
    )

    insights_text = response.choices[0].message.content

    try:
        insights = json.loads(insights_text)
    except json.JSONDecodeError:
        insights = {"raw_analysis": insights_text}

    return {
        "insights": insights,
        "event_count": len(audit_events),
        "model": OPENAI_MODEL,
        "provider": "openai",
        "generated_at": time.time(),
    }


def summarize_single_event(
    audit_event: Dict[str, Any],
    api_key: Optional[str] = None,
) -> Dict[str, Any]:
    if not api_key:
        api_key = OPENAI_API_KEY

    client = OpenAI(api_key=api_key)

    event_json = json.dumps(audit_event, indent=2)

    system_prompt = "You are a security analyst. Provide a brief, human-readable description of this federated login audit event."

    user_prompt = f"Describe this audit event in plain language:\n\n{event_json}"

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.2,
        max_tokens=256,
    )

    description = response.choices[0].message.content

    return {
        "event_id": audit_event.get("event_id", ""),
        "description": description,
        "model": OPENAI_MODEL,
        "provider": "openai",
        "generated_at": time.time(),
    }


if __name__ == "__main__":
    sample_events = [
        {
            "event_id": "evt-001",
            "event_type": "token_exchange",
            "timestamp": time.time(),
            "user_sub": "auth0|12345",
            "provider": "auth0",
            "success": True,
        },
        {
            "event_id": "evt-002",
            "event_type": "profile_fetch",
            "timestamp": time.time(),
            "user_sub": "auth0|67890",
            "provider": "auth0",
            "success": False,
            "error": "token_expired",
        },
    ]
    result = summarize_audit_events(sample_events)
    print(json.dumps(result, indent=2))
