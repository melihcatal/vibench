import os
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

from openai import OpenAI

OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")
OPENAI_API_KEY_ENV = "OPENAI_API_KEY"

@dataclass
class AuditEvent:
    provider: str
    user_id: str
    event_type: str
    timestamp: str
    success: bool
    details: Dict[str, Any]


def _client() -> OpenAI:
    api_key = os.getenv(OPENAI_API_KEY_ENV)
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return OpenAI(api_key=api_key)


def _normalize_event(event: Dict[str, Any]) -> AuditEvent:
    details = dict(event.get("details") or {})
    return AuditEvent(
        provider=str(event.get("provider") or "unknown"),
        user_id=str(event.get("user_id") or event.get("subject") or ""),
        event_type=str(event.get("event_type") or event.get("type") or "unknown"),
        timestamp=str(event.get("timestamp") or event.get("occurred_at") or datetime.now(timezone.utc).isoformat()),
        success=bool(event.get("success", True)),
        details=details,
    )


def summarize_federated_login_audit_events(events: List[Dict[str, Any]]) -> str:
    normalized = [_normalize_event(event) for event in events]
    payload = [
        {
            "provider": item.provider,
            "user_id": item.user_id,
            "event_type": item.event_type,
            "timestamp": item.timestamp,
            "success": item.success,
            "details": item.details,
        }
        for item in normalized
    ]
    client = _client()
    response = client.responses.create(
        model=OPENAI_MODEL,
        input=[
            {
                "role": "system",
                "content": "Summarize federated-login audit events for security review. Be concise and mention notable failures, patterns, and provider distribution.",
            },
            {
                "role": "user",
                "content": f"Audit events: {payload}",
            },
        ],
    )
    return response.output_text


def summarize_events(events: List[Dict[str, Any]]) -> str:
    return summarize_federated_login_audit_events(events)
