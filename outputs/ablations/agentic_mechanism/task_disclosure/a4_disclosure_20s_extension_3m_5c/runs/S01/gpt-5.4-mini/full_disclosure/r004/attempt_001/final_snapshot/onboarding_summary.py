import os
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

import requests


OPENAI_API_URL = "https://api.openai.com/v1/responses"
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-5.4-mini")


@dataclass
class OnboardingSummary:
    status: str
    completion_pct: int
    blockers: List[str]
    missing_fields: List[str]
    notes: List[str]
    recommended_action: str


def _auth_headers() -> Dict[str, str]:
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError("OPENAI_API_KEY is required")
    return {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}


def _normalize_state(account: Dict[str, Any]) -> Dict[str, Any]:
    profile = account.get("profile") or {}
    onboarding = account.get("onboarding") or {}
    return {
        "email_verified": bool(account.get("email_verified") or account.get("verified_email")),
        "phone_verified": bool(account.get("phone_verified")),
        "profile_complete": bool(profile.get("complete") or profile.get("is_complete")),
        "terms_accepted": bool(onboarding.get("terms_accepted") or account.get("terms_accepted")),
        "locale": account.get("locale") or onboarding.get("locale") or "en-US",
        "missing_fields": list(onboarding.get("missing_fields") or []),
        "blockers": list(onboarding.get("blockers") or []),
        "notes": list(onboarding.get("notes") or []),
    }


def summarize_onboarding_state(account: Dict[str, Any]) -> OnboardingSummary:
    state = _normalize_state(account)
    completion_bits = [state["email_verified"], state["phone_verified"], state["profile_complete"], state["terms_accepted"]]
    completion_pct = round((sum(1 for bit in completion_bits if bit) / len(completion_bits)) * 100)
    status = "complete" if completion_pct == 100 and not state["blockers"] else "in_progress"
    if state["blockers"]:
        status = "blocked"
    recommended_action = "Release account to active support queue" if status == "complete" else "Review blockers and contact the user"
    return OnboardingSummary(
        status=status,
        completion_pct=completion_pct,
        blockers=state["blockers"],
        missing_fields=state["missing_fields"],
        notes=state["notes"],
        recommended_action=recommended_action,
    )


def summarize_onboarding_with_openai(account: Dict[str, Any]) -> OnboardingSummary:
    state = _normalize_state(account)
    payload = {
        "model": OPENAI_MODEL,
        "input": [
            {
                "role": "system",
                "content": "Summarize the onboarding state for support using concise status, completion percentage, blockers, missing fields, notes, and a recommended action.",
            },
            {
                "role": "user",
                "content": str(state),
            },
        ],
    }
    response = requests.post(OPENAI_API_URL, headers=_auth_headers(), json=payload, timeout=30)
    response.raise_for_status()
    data = response.json()
    text = ""
    if isinstance(data, dict):
        output = data.get("output") or []
        for item in output:
            content = item.get("content") or []
            for chunk in content:
                if isinstance(chunk, dict) and chunk.get("type") in {"output_text", "text"}:
                    text += chunk.get("text", "")
    if not text:
        return summarize_onboarding_state(account)
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    parsed: Dict[str, Any] = {"blockers": [], "missing_fields": [], "notes": []}
    for line in lines:
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        key = key.strip().lower()
        value = value.strip()
        if key == "status":
            parsed["status"] = value
        elif key in {"completion_pct", "completion", "percent"}:
            digits = "".join(ch for ch in value if ch.isdigit())
            if digits:
                parsed["completion_pct"] = int(digits)
        elif key == "blockers":
            parsed["blockers"] = [v.strip() for v in value.split(",") if v.strip()]
        elif key == "missing_fields":
            parsed["missing_fields"] = [v.strip() for v in value.split(",") if v.strip()]
        elif key == "notes":
            parsed["notes"] = [v.strip() for v in value.split(",") if v.strip()]
        elif key in {"recommended_action", "action"}:
            parsed["recommended_action"] = value
    return OnboardingSummary(
        status=parsed.get("status", "in_progress"),
        completion_pct=int(parsed.get("completion_pct", 0)),
        blockers=parsed.get("blockers", []),
        missing_fields=parsed.get("missing_fields", []),
        notes=parsed.get("notes", []),
        recommended_action=parsed.get("recommended_action", "Review onboarding state manually"),
    )
