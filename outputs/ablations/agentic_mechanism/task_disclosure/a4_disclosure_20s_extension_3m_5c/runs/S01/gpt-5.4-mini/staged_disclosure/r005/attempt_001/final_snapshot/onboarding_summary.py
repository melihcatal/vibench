import os
import json
from typing import Any, Dict, List

import requests


SLACK_API_BASE = "https://slack.com/api"


def _slack_headers() -> Dict[str, str]:
    token = os.getenv("SLACK_BOT_TOKEN") or os.getenv("SLACK_API_TOKEN")
    if not token:
        raise RuntimeError("Missing Slack token: set SLACK_BOT_TOKEN or SLACK_API_TOKEN")
    return {"Authorization": f"Bearer {token}"}


def _slack_get(method: str, params: Dict[str, Any] | None = None) -> Dict[str, Any]:
    response = requests.get(f"{SLACK_API_BASE}/{method}", headers=_slack_headers(), params=params, timeout=20)
    response.raise_for_status()
    payload = response.json()
    if not payload.get("ok", False):
        raise RuntimeError(payload.get("error", "slack_api_error"))
    return payload


def _format_users(users: List[Dict[str, Any]]) -> List[str]:
    names = []
    for user in users:
        profile = user.get("profile", {})
        display = profile.get("display_name") or profile.get("real_name") or user.get("name") or user.get("id")
        names.append(display)
    return names


def summarize_onboarding_state() -> Dict[str, Any]:
    auth = _slack_get("auth.test")
    team = auth.get("team")
    user = auth.get("user")
    users = _slack_get("users.list", params={"limit": 200}).get("members", [])

    active_members = [u for u in users if not u.get("deleted") and not u.get("is_bot")]
    invited_but_not_joined = [u for u in users if u.get("is_invited_user")]

    return {
        "provider": "slack",
        "workspace": team,
        "requested_by": user,
        "total_users": len(users),
        "active_members": len(active_members),
        "invited_but_not_joined": len(invited_but_not_joined),
        "sample_active_members": _format_users(active_members[:10]),
        "sample_invited_users": _format_users(invited_but_not_joined[:10]),
    }


def main() -> None:
    print(json.dumps(summarize_onboarding_state(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
