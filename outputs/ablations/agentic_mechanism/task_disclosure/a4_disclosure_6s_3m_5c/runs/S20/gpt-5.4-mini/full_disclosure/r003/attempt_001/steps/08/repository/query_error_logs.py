import os
from datetime import datetime, timezone

import requests


def query_error_logs(severity: str, start_time: str, end_time: str, limit: int = 100):
    api_key = os.getenv("SENTRY_AUTH_TOKEN")
    organization = os.getenv("SENTRY_ORG_SLUG")
    project = os.getenv("SENTRY_PROJECT_SLUG")
    if not api_key or not organization or not project:
        raise RuntimeError("Missing Sentry configuration")

    url = f"https://sentry.io/api/0/projects/{organization}/{project}/issues/"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Accept": "application/json",
    }
    params = {
        "query": f'level:{severity} firstSeen:>={start_time} lastSeen:<={end_time}',
        "limit": limit,
    }
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _to_iso8601(dt: datetime) -> str:
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return dt.astimezone(timezone.utc).isoformat().replace("+00:00", "Z")


if __name__ == "__main__":
    now = datetime.now(timezone.utc)
    start = _to_iso8601(now.replace(hour=0, minute=0, second=0, microsecond=0))
    end = _to_iso8601(now)
    print(query_error_logs("error", start, end))
