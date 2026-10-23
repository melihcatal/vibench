import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, Iterable, List, Mapping, Optional

from google.cloud import logging_v2


GOOGLE_CLOUD_LOGGING_PROJECT_ENV = "GOOGLE_CLOUD_PROJECT"
GOOGLE_CLOUD_KMS_KEY_NAME_ENV = "GOOGLE_CLOUD_KMS_KEY_NAME"
DEFAULT_LOOKBACK_HOURS = 24


@dataclass(frozen=True)
class CryptoEvent:
    key_name: str
    method: str
    count: int
    timestamp: Optional[str] = None
    principal: Optional[str] = None


def _env(name: str) -> Optional[str]:
    import os

    value = os.getenv(name)
    return value if value else None


def _client() -> logging_v2.Client:
    project_id = _env(GOOGLE_CLOUD_LOGGING_PROJECT_ENV)
    return logging_v2.Client(project=project_id) if project_id else logging_v2.Client()


def _parse_event(entry: Mapping[str, Any]) -> Optional[CryptoEvent]:
    payload = entry.get("jsonPayload") or entry.get("protoPayload") or {}
    if isinstance(payload, str):
        try:
            payload = json.loads(payload)
        except json.JSONDecodeError:
            return None
    if not isinstance(payload, Mapping):
        return None

    key_name = payload.get("resourceName") or payload.get("keyName") or payload.get("name")
    method = payload.get("methodName") or payload.get("operation") or payload.get("action")
    if not key_name or not method:
        return None

    count = payload.get("count", 1)
    try:
        count = int(count)
    except (TypeError, ValueError):
        count = 1

    timestamp = entry.get("timestamp") or payload.get("timestamp")
    principal = payload.get("principalEmail") or payload.get("authenticationInfo", {}).get("principalEmail") if isinstance(payload.get("authenticationInfo"), Mapping) else payload.get("principalEmail")
    return CryptoEvent(str(key_name), str(method), count, str(timestamp) if timestamp else None, str(principal) if principal else None)


def fetch_crypto_events(key_name: Optional[str] = None, lookback_hours: int = DEFAULT_LOOKBACK_HOURS) -> List[CryptoEvent]:
    resolved_key = key_name or _env(GOOGLE_CLOUD_KMS_KEY_NAME_ENV)
    if not resolved_key:
        raise ValueError(f"Missing required environment variable: {GOOGLE_CLOUD_KMS_KEY_NAME_ENV}")

    client = _client()
    query = f'resource.type="cloudkms_key" AND (protoPayload.resourceName:"{resolved_key}" OR jsonPayload.resourceName:"{resolved_key}" OR jsonPayload.keyName:"{resolved_key}")'
    if lookback_hours > 0:
        query = f'{query} AND timestamp >= "{datetime.utcnow().isoformat()}Z"'

    events: List[CryptoEvent] = []
    for entry in client.list_entries(filter_=query, order_by=logging_v2.DESCENDING, page_size=1000):
        parsed = _parse_event(entry)
        if parsed:
            events.append(parsed)
    return events


def summarize_key_usage(events: Iterable[CryptoEvent]) -> Dict[str, Any]:
    by_method = Counter()
    by_key = Counter()
    principals = Counter()
    total = 0

    for event in events:
        by_method[event.method] += event.count
        by_key[event.key_name] += event.count
        if event.principal:
            principals[event.principal] += event.count
        total += event.count

    return {
        "total_events": total,
        "by_method": dict(sorted(by_method.items())),
        "by_key": dict(sorted(by_key.items())),
        "top_principals": principals.most_common(10),
    }


def generate_key_usage_summary(key_name: Optional[str] = None, lookback_hours: int = DEFAULT_LOOKBACK_HOURS) -> Dict[str, Any]:
    events = fetch_crypto_events(key_name=key_name, lookback_hours=lookback_hours)
    return summarize_key_usage(events)
