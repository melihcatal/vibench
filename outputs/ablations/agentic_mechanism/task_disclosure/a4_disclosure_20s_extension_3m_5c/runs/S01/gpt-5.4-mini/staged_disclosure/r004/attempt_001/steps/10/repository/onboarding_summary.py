import os
from typing import Any, Dict, List, Optional

import requests


INTERCOM_BASE_URL = "https://api.intercom.io"


def _headers() -> Dict[str, str]:
    token = os.environ.get("INTERCOM_ACCESS_TOKEN")
    if not token:
        raise RuntimeError("INTERCOM_ACCESS_TOKEN is required")
    return {
        "Authorization": f"Bearer {token}",
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Intercom-Version": os.environ.get("INTERCOM_API_VERSION", "2.11"),
    }


def _get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    response = requests.get(f"{INTERCOM_BASE_URL}{path}", headers=_headers(), params=params, timeout=30)
    response.raise_for_status()
    return response.json()


def _first_value(items: List[Dict[str, Any]], keys: List[str]) -> Optional[Any]:
    for item in items:
        value = item.get("value")
        if item.get("field") in keys or item.get("name") in keys:
            return value
    return None


def summarize_onboarding_state(user_id: Optional[str] = None, email: Optional[str] = None) -> Dict[str, Any]:
    if not user_id and not email:
        raise ValueError("user_id or email is required")

    query = {"email": email} if email else {"user_id": user_id}
    contact = _get("/contacts", params=query)
    data = contact.get("data", [])
    if not data:
        return {"found": False, "provider": "intercom"}

    record = data[0]
    custom_attributes = record.get("custom_attributes", {}) or {}
    tags = [tag.get("name") for tag in record.get("tags", {}).get("tags", []) if tag.get("name")]

    onboarding_steps = {
        "account_created": bool(record.get("created_at")),
        "email_verified": bool(custom_attributes.get("email_verified") or custom_attributes.get("verified_email")),
        "profile_completed": bool(custom_attributes.get("profile_completed") or custom_attributes.get("onboarding_complete")),
        "product_activated": bool(custom_attributes.get("product_activated") or custom_attributes.get("activated")),
    }

    summary = {
        "found": True,
        "provider": "intercom",
        "contact_id": record.get("id"),
        "email": record.get("email"),
        "name": record.get("name"),
        "segments": tags,
        "onboarding_state": onboarding_steps,
        "last_seen_at": record.get("last_seen_at"),
        "created_at": record.get("created_at"),
        "plan": custom_attributes.get("plan") or _first_value(record.get("custom_attributes", []), ["plan"]),
    }

    completed = sum(1 for value in onboarding_steps.values() if value)
    summary["completion_ratio"] = f"{completed}/{len(onboarding_steps)}"
    summary["needs_attention"] = [step for step, done in onboarding_steps.items() if not done]
    return summary


if __name__ == "__main__":
    import json
    import sys

    kwargs = {}
    if len(sys.argv) > 1:
        kwargs["user_id"] = sys.argv[1]
    if len(sys.argv) > 2:
        kwargs["email"] = sys.argv[2]
    print(json.dumps(summarize_onboarding_state(**kwargs), indent=2, sort_keys=True))
