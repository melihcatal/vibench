import json
import os
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

from google.cloud import logging_v2


@dataclass(frozen=True)
class KeyUsageEvent:
    event_type: str
    timestamp: str
    key_name: str
    principal: Optional[str] = None
    status: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class GoogleCloudLoggingProvider:
    def __init__(self, project_id: Optional[str] = None) -> None:
        self.project_id = project_id or os.environ.get("GOOGLE_CLOUD_PROJECT")
        self.client = logging_v2.Client(project=self.project_id)

    def fetch_entries(self, resource_names: Optional[Iterable[str]] = None, page_size: int = 100) -> List[Dict[str, Any]]:
        entries: List[Dict[str, Any]] = []
        iterator = self.client.list_entries(resource_names=resource_names, page_size=page_size)
        for entry in iterator:
            payload = dict(entry.payload) if isinstance(entry.payload, dict) else {"message": entry.payload}
            entries.append(
                {
                    "timestamp": entry.timestamp.isoformat() if entry.timestamp else None,
                    "log_name": entry.log_name,
                    "resource_type": getattr(entry.resource, "type", None),
                    "resource_labels": dict(getattr(entry.resource, "labels", {}) or {}),
                    "severity": entry.severity.name if getattr(entry, "severity", None) else None,
                    "payload": payload,
                }
            )
        return entries


def _normalize_timestamp(value: Optional[str]) -> str:
    if value:
        return value
    return datetime.now(timezone.utc).isoformat()


def summarize_key_usage(log_entries: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    events: List[KeyUsageEvent] = []
    for entry in log_entries:
        payload = entry.get("payload", {})
        if not isinstance(payload, dict):
            payload = {"message": payload}
        message = json.dumps(payload, sort_keys=True)
        lowered = message.lower()
        if any(token in lowered for token in ("encrypt", "decrypt", "asymmetric_sign", "asymmetric_verify", "crypto key", "kms")):
            event_type = next((name for name in ("encrypt", "decrypt", "sign", "verify") if name in lowered), "crypto_event")
            events.append(
                KeyUsageEvent(
                    event_type=event_type,
                    timestamp=_normalize_timestamp(entry.get("timestamp")),
                    key_name=str(payload.get("key") or payload.get("key_name") or entry.get("log_name") or "unknown"),
                    principal=payload.get("principalEmail") or payload.get("principal") or payload.get("authenticationInfo", {}).get("principalEmail"),
                    status=payload.get("status") or entry.get("severity"),
                    metadata={k: v for k, v in payload.items() if k not in {"key", "key_name", "principalEmail", "principal", "authenticationInfo", "status"}},
                )
            )

    total = len(events)
    by_type: Dict[str, int] = {}
    by_principal: Dict[str, int] = {}
    for event in events:
        by_type[event.event_type] = by_type.get(event.event_type, 0) + 1
        if event.principal:
            by_principal[event.principal] = by_principal.get(event.principal, 0) + 1

    return {
        "total_events": total,
        "by_type": by_type,
        "by_principal": by_principal,
        "events": [event.__dict__ for event in events],
    }


def main() -> None:
    provider = GoogleCloudLoggingProvider()
    entries = provider.fetch_entries()
    summary = summarize_key_usage(entries)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
