import json
import os
from collections import Counter, defaultdict
from datetime import datetime, timezone
from typing import Any, Dict, Iterable, List, Optional

import requests


OKTA_DOMAIN_ENV = "OKTA_DOMAIN"
OKTA_API_TOKEN_ENV = "OKTA_API_TOKEN"
OKTA_AUDIT_API_PATH = "/api/v1/logs"


def _okta_headers() -> Dict[str, str]:
    token = os.getenv(OKTA_API_TOKEN_ENV)
    if not token:
        raise ValueError("Missing OKTA_API_TOKEN")
    return {"Authorization": f"SSWS {token}", "Accept": "application/json"}


def fetch_okta_audit_events(limit: int = 200) -> List[Dict[str, Any]]:
    domain = os.getenv(OKTA_DOMAIN_ENV)
    if not domain:
        raise ValueError("Missing OKTA_DOMAIN")
    url = domain.rstrip("/") + OKTA_AUDIT_API_PATH
    params = {"limit": min(max(limit, 1), 1000)}
    response = requests.get(url, headers=_okta_headers(), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _event_timestamp(event: Dict[str, Any]) -> Optional[datetime]:
    raw = event.get("published") or event.get("timestamp") or event.get("eventTime")
    if not raw:
        return None
    try:
        return datetime.fromisoformat(raw.replace("Z", "+00:00")).astimezone(timezone.utc)
    except Exception:
        return None


def summarize_federated_login_events(events: Iterable[Dict[str, Any]]) -> Dict[str, Any]:
    total = 0
    by_outcome = Counter()
    by_idp = Counter()
    by_user = Counter()
    by_day = Counter()
    providers = defaultdict(int)

    for event in events:
        etype = str(event.get("eventType", "")).lower()
        debug_context = event.get("debugContext", {}) or {}
        outcome = (event.get("outcome") or {}).get("result", "UNKNOWN")
        actor = (event.get("actor") or {}).get("alternateId") or (event.get("actor") or {}).get("displayName") or "unknown"
        ts = _event_timestamp(event)

        if not any(key in etype for key in ("sso", "federat", "social", "openid", "saml")):
            continue

        total += 1
        by_outcome[outcome] += 1
        by_user[actor] += 1

        idp = debug_context.get("debugData", {}).get("identityProvider") or event.get("client", {}).get("userAgent", {}).get("rawUserAgent") or "unknown"
        by_idp[idp] += 1
        providers[idp] += 1

        if ts:
            by_day[ts.date().isoformat()] += 1

    return {
        "total_federated_login_events": total,
        "outcomes": dict(by_outcome),
        "identity_providers": dict(by_idp),
        "top_users": by_user.most_common(10),
        "events_by_day": dict(sorted(by_day.items())),
        "provider_signals": dict(providers),
    }


def main() -> None:
    events = fetch_okta_audit_events()
    summary = summarize_federated_login_events(events)
    print(json.dumps(summary, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
