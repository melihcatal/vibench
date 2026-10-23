from collections import Counter
from typing import Iterable, Mapping

import requests


def summarize_federated_login_audit(events: Iterable[Mapping[str, str]]) -> dict:
    counter = Counter(event.get("provider", "unknown") for event in events)
    return {"total": sum(counter.values()), "by_provider": dict(counter)}


def fetch_google_cloud_audit_summary(project_id: str, access_token: str) -> dict:
    url = f"https://logging.googleapis.com/v2/projects/{project_id}/entries:list"
    response = requests.post(
        url,
        headers={"Authorization": f"Bearer {access_token}"},
        json={"pageSize": 100},
        timeout=30,
    )
    response.raise_for_status()
    return response.json()
