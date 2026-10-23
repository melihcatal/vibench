import os
import json
from typing import List, Optional
from datetime import datetime, timezone

import anthropic

from identity_models import AuditEvent, AuditSummary


ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
ANTHROPIC_MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-20250514")


def create_anthropic_client() -> anthropic.Anthropic:
    return anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)


def summarize_audit_events(
    events: List[AuditEvent],
    model: str = None,
    max_tokens: int = 2048,
) -> AuditSummary:
    if model is None:
        model = ANTHROPIC_MODEL

    client = create_anthropic_client()

    successful = sum(1 for e in events if e.status == "success")
    failed = sum(1 for e in events if e.status == "failure")
    unique_users = len(set(e.user_sub for e in events if e.user_sub))

    providers = {}
    for e in events:
        providers[e.provider] = providers.get(e.provider, 0) + 1

    risk_events = [e for e in events if e.risk_score > 0.5]

    events_json = json.dumps([e.to_dict() for e in events], indent=2)

    system_prompt = (
        "You are a security analyst summarizing federated login audit events. "
        "Provide a concise summary highlighting patterns, anomalies, and risk indicators."
    )

    user_prompt = (
        f"Summarize the following {len(events)} federated login audit events:\n\n"
        f"{events_json}\n\n"
        f"Include: total events, success/failure rates, unique users, "
        f"provider distribution, notable risk events, and any security recommendations."
    )

    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    summary_text = ""
    if message.content:
        for block in message.content:
            if hasattr(block, "text"):
                summary_text += block.text

    return AuditSummary(
        total_events=len(events),
        successful_logins=successful,
        failed_logins=failed,
        unique_users=unique_users,
        providers=providers,
        risk_events=[e.to_dict() for e in risk_events],
        summary_text=summary_text,
        generated_at=datetime.now(timezone.utc).isoformat(),
    )


def summarize_events_from_dicts(
    events_data: List[dict],
    model: str = None,
    max_tokens: int = 2048,
) -> AuditSummary:
    events = [AuditEvent(**e) for e in events_data]
    return summarize_audit_events(events, model=model, max_tokens=max_tokens)


def generate_risk_assessment(
    events: List[AuditEvent],
    model: str = None,
) -> dict:
    if model is None:
        model = ANTHROPIC_MODEL

    client = create_anthropic_client()

    high_risk = [e for e in events if e.risk_score > 0.7]
    events_json = json.dumps([e.to_dict() for e in high_risk[:20]], indent=2)

    system_prompt = (
        "You are a security analyst assessing federated login risk. "
        "Provide a risk assessment based on high-risk login events."
    )

    user_prompt = (
        f"Assess the risk of these {len(high_risk)} high-risk federated login events:\n\n"
        f"{events_json}\n\n"
        f"Provide: overall risk level, key risk factors, "
        f"recommended actions, and affected user patterns."
    )

    message = client.messages.create(
        model=model,
        max_tokens=1024,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )

    assessment_text = ""
    if message.content:
        for block in message.content:
            if hasattr(block, "text"):
                assessment_text += block.text

    return {
        "risk_level": "high"
        if len(high_risk) > 5
        else "medium"
        if len(high_risk) > 0
        else "low",
        "high_risk_count": len(high_risk),
        "assessment": assessment_text,
        "model": model,
        "provider": "anthropic",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }
