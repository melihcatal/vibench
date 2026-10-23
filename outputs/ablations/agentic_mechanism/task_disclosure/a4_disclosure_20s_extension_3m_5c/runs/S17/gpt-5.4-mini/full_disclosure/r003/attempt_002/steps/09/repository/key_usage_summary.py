import argparse
import os
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

import requests


GOOGLE_CLOUD_AUDIT_URL = "https://logging.googleapis.com/v2/entries:list"


@dataclass
class KeyUsageSummary:
    provider: str
    key_name: Optional[str]
    total_events: int
    encrypt_events: int
    decrypt_events: int
    sign_events: int
    verify_events: int
    latest_event_time: Optional[str]
    latest_event_type: Optional[str]
    raw_events: List[Dict[str, Any]]


def _access_token() -> str:
    token = os.getenv("GOOGLE_OAUTH_ACCESS_TOKEN") or os.getenv("GOOGLE_CLOUD_ACCESS_TOKEN")
    if not token:
        raise ValueError("Missing GOOGLE_OAUTH_ACCESS_TOKEN or GOOGLE_CLOUD_ACCESS_TOKEN")
    return token


def _headers() -> Dict[str, str]:
    return {"Authorization": f"Bearer {_access_token()}", "Content-Type": "application/json"}


def _parse_time(value: str) -> datetime:
    if value.endswith("Z"):
        value = value[:-1] + "+00:00"
    return datetime.fromisoformat(value)


def _event_type(entry: Dict[str, Any]) -> Optional[str]:
    proto = entry.get("protoPayload", {}) if isinstance(entry.get("protoPayload"), dict) else {}
    method = str(proto.get("methodName", "")).lower()
    if "encrypt" in method:
        return "encrypt"
    if "decrypt" in method:
        return "decrypt"
    if "sign" in method:
        return "sign"
    if "verify" in method:
        return "verify"
    return None


def _extract_key_name(entry: Dict[str, Any]) -> Optional[str]:
    proto = entry.get("protoPayload", {}) if isinstance(entry.get("protoPayload"), dict) else {}
    resource = proto.get("resourceName")
    return resource if isinstance(resource, str) and resource else None


def summarize_key_usage(project_id: str, key_name: Optional[str] = None, page_size: int = 50) -> KeyUsageSummary:
    body: Dict[str, Any] = {
        "resourceNames": [f"projects/{project_id}"],
        "pageSize": page_size,
        "filter": 'protoPayload.serviceName="cloudkms.googleapis.com"',
    }
    response = requests.post(GOOGLE_CLOUD_AUDIT_URL, headers=_headers(), json=body, timeout=30)
    response.raise_for_status()
    entries = response.json().get("entries", [])

    filtered: List[Dict[str, Any]] = []
    counts = {"encrypt": 0, "decrypt": 0, "sign": 0, "verify": 0}
    latest_time: Optional[datetime] = None
    latest_type: Optional[str] = None

    for entry in entries:
        if not isinstance(entry, dict):
            continue
        resource_name = _extract_key_name(entry)
        if key_name and resource_name and key_name not in resource_name:
            continue
        event_type = _event_type(entry)
        if event_type:
            counts[event_type] += 1
        filtered.append(entry)
        timestamp = entry.get("timestamp")
        if isinstance(timestamp, str):
            parsed = _parse_time(timestamp)
            if latest_time is None or parsed > latest_time:
                latest_time = parsed
                latest_type = event_type

    return KeyUsageSummary(
        provider="google-cloud-logging/google-cloud-kms",
        key_name=key_name,
        total_events=len(filtered),
        encrypt_events=counts["encrypt"],
        decrypt_events=counts["decrypt"],
        sign_events=counts["sign"],
        verify_events=counts["verify"],
        latest_event_time=latest_time.isoformat() if latest_time else None,
        latest_event_type=latest_type,
        raw_events=filtered,
    )


def _main() -> None:
    parser = argparse.ArgumentParser(description="Summarize key usage and crypto events from Google Cloud audit logs.")
    parser.add_argument("--project-id", required=True)
    parser.add_argument("--key-name")
    parser.add_argument("--page-size", type=int, default=50)
    args = parser.parse_args()
    summary = summarize_key_usage(args.project_id, key_name=args.key_name, page_size=args.page_size)
    print(asdict(summary))


if __name__ == "__main__":
    _main()
