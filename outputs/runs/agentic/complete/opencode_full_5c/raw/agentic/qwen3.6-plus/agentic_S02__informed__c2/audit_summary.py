import os
import json
from typing import List, Dict, Any
from openai import OpenAI
from identity_models import AuditEvent, AuditSummary


def summarize_audit_events(
    events: List[Dict[str, Any]],
    model: str = "gpt-4o",
    api_key: str | None = None,
) -> AuditSummary:
    if api_key is None:
        api_key = os.getenv("OPENAI_API_KEY", "")

    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable is required")

    client = OpenAI(api_key=api_key)

    successful = sum(1 for e in events if e.get("status") == "success")
    failed = sum(1 for e in events if e.get("status") == "failure")
    unique_users = len(set(e.get("user_id", "") for e in events if e.get("user_id")))
    unique_providers = len(
        set(e.get("provider", "") for e in events if e.get("provider"))
    )
    timestamps = sorted(e.get("timestamp", "") for e in events if e.get("timestamp"))

    events_json = json.dumps(events[:50], indent=2)

    prompt = (
        f"Analyze the following federated-login audit events and provide a concise summary.\n\n"
        f"Total events: {len(events)}\n"
        f"Successful logins: {successful}\n"
        f"Failed logins: {failed}\n"
        f"Unique users: {unique_users}\n"
        f"Unique providers: {unique_providers}\n\n"
        f"Audit events (JSON):\n{events_json}\n\n"
        f"Provide a brief summary paragraph highlighting:\n"
        f"1. Overall login activity patterns\n"
        f"2. Any security concerns or anomalies\n"
        f"3. Provider usage distribution\n"
        f"4. Recommendations if any failures were detected"
    )

    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a security analyst specializing in federated identity and OAuth/OIDC login flows. Provide concise, actionable audit summaries.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=500,
    )

    summary_text = response.choices[0].message.content.strip()

    risk_flags = []
    for event in events:
        if event.get("risk_score", 0) > 0.7:
            risk_flags.append(
                {
                    "event_id": event.get("event_id"),
                    "user_id": event.get("user_id"),
                    "risk_score": event.get("risk_score"),
                    "event_type": event.get("event_type"),
                    "details": event.get("details", {}),
                }
            )

    return AuditSummary(
        total_events=len(events),
        successful_logins=successful,
        failed_logins=failed,
        unique_users=unique_users,
        unique_providers=unique_providers,
        time_range_start=timestamps[0] if timestamps else "",
        time_range_end=timestamps[-1] if timestamps else "",
        summary_text=summary_text,
        risk_flags=risk_flags,
    )


def generate_audit_report(
    events: List[AuditEvent],
    model: str = "gpt-4o",
) -> str:
    events_dicts = [e.to_dict() for e in events]
    summary = summarize_audit_events(events_dicts, model=model)
    return summary.summary_text


if __name__ == "__main__":
    sample_events = [
        {
            "event_id": "evt-001",
            "event_type": "login_completed",
            "timestamp": "2026-04-18T10:00:00Z",
            "user_id": "auth0|user123",
            "provider": "auth0",
            "status": "success",
            "ip_address": "192.168.1.1",
            "risk_score": 0.1,
        },
        {
            "event_id": "evt-002",
            "event_type": "login_failed",
            "timestamp": "2026-04-18T10:05:00Z",
            "user_id": "auth0|user456",
            "provider": "auth0",
            "status": "failure",
            "ip_address": "10.0.0.1",
            "risk_score": 0.8,
        },
    ]
    summary = summarize_audit_events(sample_events)
    print(summary.summary_text)
