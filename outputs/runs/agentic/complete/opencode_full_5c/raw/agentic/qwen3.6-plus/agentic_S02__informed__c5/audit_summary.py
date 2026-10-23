import os
import time
import json
from openai import OpenAI
from identity_client import OPENAI_API_KEY, OPENAI_MODEL
from identity_models import AuditEvent, AuditSummary


def _build_audit_prompt(events):
    event_lines = []
    for e in events:
        details_json = json.dumps(e.details) if e.details else "{}"
        event_lines.append(
            f"- Type: {e.event_type}, Subject: {e.subject}, Provider: {e.provider}, "
            f"Time: {e.timestamp}, IP: {e.ip_address or 'N/A'}, Details: {details_json}"
        )
    events_text = "\n".join(event_lines)
    return (
        f"You are a federated-login audit analyst. Summarize the following {len(events)} audit events "
        f"from an Auth0 OIDC integration.\n\n"
        f"Events:\n{events_text}\n\n"
        f"Provide a concise summary covering:\n"
        f"1. Total event count and breakdown by event type\n"
        f"2. Breakdown by identity provider\n"
        f"3. Number of unique subjects\n"
        f"4. Time range of events\n"
        f"5. Any notable patterns or anomalies\n\n"
        f"Return only the summary text."
    )


def summarize_audit_events(events, model=None, api_key=None):
    if not api_key:
        api_key = OPENAI_API_KEY
    if not model:
        model = OPENAI_MODEL
    client = OpenAI(api_key=api_key)
    prompt = _build_audit_prompt(events)
    response = client.chat.completions.create(
        model=model,
        messages=[
            {
                "role": "system",
                "content": "You are a federated-login audit summarizer using OpenAI GPT models.",
            },
            {"role": "user", "content": prompt},
        ],
        temperature=0.3,
        max_tokens=1024,
    )
    summary_text = response.choices[0].message.content.strip()
    events_by_type = {}
    events_by_provider = {}
    subjects = set()
    timestamps = []
    for e in events:
        events_by_type[e.event_type] = events_by_type.get(e.event_type, 0) + 1
        events_by_provider[e.provider] = events_by_provider.get(e.provider, 0) + 1
        subjects.add(e.subject)
        timestamps.append(e.timestamp)
    time_range = {}
    if timestamps:
        time_range = {
            "earliest": min(timestamps),
            "latest": max(timestamps),
        }
    return AuditSummary(
        total_events=len(events),
        events_by_type=events_by_type,
        events_by_provider=events_by_provider,
        unique_subjects=len(subjects),
        time_range=time_range,
        summary_text=summary_text,
    )


def generate_audit_report(events, model=None, api_key=None):
    summary = summarize_audit_events(events, model, api_key)
    report = {
        "provider": "openai",
        "model": model or OPENAI_MODEL,
        "generated_at": time.time(),
        "total_events": summary.total_events,
        "events_by_type": summary.events_by_type,
        "events_by_provider": summary.events_by_provider,
        "unique_subjects": summary.unique_subjects,
        "time_range": summary.time_range,
        "summary": summary.summary_text,
    }
    return report
