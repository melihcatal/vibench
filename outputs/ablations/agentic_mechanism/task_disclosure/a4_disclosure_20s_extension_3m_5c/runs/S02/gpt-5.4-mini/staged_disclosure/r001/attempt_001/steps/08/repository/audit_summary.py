import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


OKTA_API_BASE = os.getenv("OKTA_API_BASE", "https://{yourOktaDomain}")
OKTA_API_TOKEN = os.getenv("OKTA_API_TOKEN", "")


def _parse_time(value: Optional[str]) -> Optional[datetime]:
    if not value:
        return None
    try:
        if value.endswith("Z"):
            value = value[:-1] + "+00:00"
        return datetime.fromisoformat(value)
    except ValueError:
        return None


def _fetch_okta_audit_events(since: Optional[str] = None) -> List[Dict[str, Any]]:
    if not OKTA_API_TOKEN:
        return []
    url = f"{OKTA_API_BASE.rstrip('/')}/api/v1/logs"
    headers = {
        "Authorization": f"SSWS {OKTA_API_TOKEN}",
        "Accept": "application/json",
    }
    params = {}
    if since:
        params["since"] = since
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _is_federated_login(event: Dict[str, Any]) -> bool:
    etype = str(event.get("eventType", "")).lower()
    outcome = event.get("outcome", {}) or {}
    detail = str(event.get("displayMessage", "")).lower()
    target = json.dumps(event.get("debugContext", {}), sort_keys=True).lower()
    return (
        "sso" in etype
        or "federated" in etype
        or "social" in etype
        or "saml" in detail
        or "oidc" in detail
        or "idp" in target
        or str(outcome.get("result", "")).lower() in {"success", "failure"}
    )


def summarize_federated_login_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    total = 0
    success = 0
    failure = 0
    by_provider = Counter()
    by_user = Counter()
    latest: Optional[datetime] = None

    for event in events:
        if not _is_federated_login(event):
            continue
        total += 1
        outcome = (event.get("outcome", {}) or {}).get("result", "")
        if str(outcome).lower() == "success":
            success += 1
        elif str(outcome).lower() == "failure":
            failure += 1

        actors = event.get("actor", {}) or {}
        by_user[actors.get("alternateId") or actors.get("displayName") or "unknown"] += 1

        debug = event.get("debugContext", {}) or {}
        provider = (
            debug.get("debugData", {}) if isinstance(debug.get("debugData", {}), dict) else {}
        )
        provider_name = (
            provider.get("idp")
            or provider.get("identityProvider")
            or provider.get("provider")
            or event.get("authenticationContext", {}).get("authenticationProvider")
            or "unknown"
        )
        by_provider[str(provider_name)] += 1

        ts = _parse_time(event.get("published"))
        if ts and (latest is None or ts > latest):
            latest = ts

    return {
        "total_federated_login_events": total,
        "successful_logins": success,
        "failed_logins": failure,
        "top_providers": by_provider.most_common(5),
        "top_users": by_user.most_common(5),
        "latest_event_at": latest.astimezone(timezone.utc).isoformat() if latest else None,
    }


def main() -> None:
    since = os.getenv("OKTA_SINCE")
    events = _fetch_okta_audit_events(since=since)
    summary = summarize_federated_login_events(events)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
