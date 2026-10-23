import os
from dataclasses import dataclass
from typing import Dict


@dataclass(frozen=True)
class IdentitySettings:
    api_key: str
    timeout_seconds: float = 20.0
    user_agent: str = "email-password-lifecycle/1.0"


def get_identity_settings() -> IdentitySettings:
    api_key = os.getenv("FIREBASE_WEB_API_KEY") or os.getenv("GOOGLE_API_KEY") or os.getenv("IDENTITY_TOOLKIT_API_KEY")
    if not api_key:
        raise RuntimeError("Missing required API key in FIREBASE_WEB_API_KEY, GOOGLE_API_KEY, or IDENTITY_TOOLKIT_API_KEY")
    timeout = float(os.getenv("IDENTITY_HTTP_TIMEOUT_SECONDS", "20"))
    user_agent = os.getenv("IDENTITY_USER_AGENT", "email-password-lifecycle/1.0")
    return IdentitySettings(api_key=api_key, timeout_seconds=timeout, user_agent=user_agent)


def json_headers() -> Dict[str, str]:
    return {"Content-Type": "application/json"}


def form_headers() -> Dict[str, str]:
    return {"Content-Type": "application/x-www-form-urlencoded"}


def user_agent_headers(headers: Dict[str, str]) -> Dict[str, str]:
    settings = get_identity_settings()
    merged = dict(headers)
    merged["User-Agent"] = settings.user_agent
    return merged
