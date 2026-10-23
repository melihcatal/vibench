import os
from datetime import datetime, timezone

import requests


GITLAB_API_BASE = "https://gitlab.com/api/v4"


def _headers():
    token = os.getenv("GITLAB_TOKEN")
    if not token:
        raise RuntimeError("GITLAB_TOKEN is required")
    return {"PRIVATE-TOKEN": token}


def _get(path, params=None):
    response = requests.get(f"{GITLAB_API_BASE}{path}", headers=_headers(), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _paginate(path, params=None):
    page = 1
    items = []
    params = dict(params or {})
    params.setdefault("per_page", 100)
    while True:
        params["page"] = page
        response = requests.get(f"{GITLAB_API_BASE}{path}", headers=_headers(), params=params, timeout=30)
        response.raise_for_status()
        batch = response.json()
        if not batch:
            break
        items.extend(batch)
        if len(batch) < params["per_page"]:
            break
        page += 1
    return items


def _days_since(date_str):
    if not date_str:
        return None
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days


def summarize_secret_rotation(group_id):
    projects = _paginate(f"/groups/{group_id}/projects", params={"include_subgroups": True, "simple": True})
    summary = []
    for project in projects:
        variables = _paginate(f"/projects/{project['id']}/variables")
        secret_vars = [v for v in variables if v.get("masked") or v.get("protected")]
        latest_update = None
        for v in secret_vars:
            updated = v.get("updated_at") or v.get("created_at")
            if updated and (latest_update is None or updated > latest_update):
                latest_update = updated
        summary.append({
            "project": project.get("path_with_namespace"),
            "secret_variable_count": len(secret_vars),
            "latest_rotation_age_days": _days_since(latest_update),
        })
    return summary


if __name__ == "__main__":
    group_id = os.getenv("GITLAB_GROUP_ID")
    if not group_id:
        raise RuntimeError("GITLAB_GROUP_ID is required")
    result = summarize_secret_rotation(group_id)
    for item in result:
        print(item)
