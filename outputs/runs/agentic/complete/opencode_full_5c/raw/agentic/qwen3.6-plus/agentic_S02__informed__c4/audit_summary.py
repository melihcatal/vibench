import os
import json
from typing import Optional
import anthropic
from identity_models import AuditEvent, AuditSummary


def summarize_audit_events(
    events: list[dict],
    max_tokens: int = 1024,
    model: str = "claude-3-5-sonnet-20241022",
) -> AuditSummary:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    client = anthropic.Anthropic(api_key=api_key)
    total_events = len(events)
    successful = sum(1 for e in events if e.get("success", True))
    failed = total_events - successful
    providers = {}
    for e in events:
        p = e.get("provider", "unknown")
        providers[p] = providers.get(p, 0) + 1
    user_counts = {}
    for e in events:
        sub = e.get("user_sub", "anonymous")
        user_counts[sub] = user_counts.get(sub, 0) + 1
    top_users = sorted(user_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    timestamps = [e.get("timestamp", "") for e in events if e.get("timestamp")]
    time_range = {
        "earliest": min(timestamps) if timestamps else "",
        "latest": max(timestamps) if timestamps else "",
    }
    events_json = json.dumps(events[:50], indent=2)
    system_prompt = (
        "You are a security analyst summarizing federated login audit events. "
        "Provide a concise summary highlighting patterns, anomalies, and key statistics."
    )
    user_prompt = (
        f"Summarize the following {total_events} federated-login audit events. "
        f"Successful: {successful}, Failed: {failed}. "
        f"Providers: {providers}. "
        f"Events:\n{events_json}"
    )
    message = client.messages.create(
        model=model,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}],
    )
    summary_text = ""
    for block in message.content:
        if hasattr(block, "text"):
            summary_text += block.text
    return AuditSummary(
        total_events=total_events,
        successful_logins=successful,
        failed_logins=failed,
        providers=providers,
        time_range=time_range,
        top_users=[{"sub": u, "count": c} for u, c in top_users],
        summary_text=summary_text,
    )


def generate_audit_report(
    events: list[dict],
    focus: Optional[str] = None,
    model: str = "claude-3-5-sonnet-20241022",
) -> str:
    api_key = os.environ.get("ANTHROPIC_API_KEY", "")
    if not api_key:
        raise ValueError("ANTHROPIC_API_KEY environment variable is required")
    client = anthropic.Anthropic(api_key=api_key)
    events_json = json.dumps(events[:100], indent=2)
    focus_instruction = f"Focus specifically on: {focus}" if focus else ""
    message = client.messages.create(
        model=model,
        max_tokens=2048,
        system="You are a security compliance officer generating audit reports for federated identity systems.",
        messages=[
            {
                "role": "user",
                "content": (
                    f"Generate a detailed audit report for these federated login events. "
                    f"{focus_instruction}\n\nEvents:\n{events_json}"
                ),
            }
        ],
    )
    report = ""
    for block in message.content:
        if hasattr(block, "text"):
            report += block.text
    return report
