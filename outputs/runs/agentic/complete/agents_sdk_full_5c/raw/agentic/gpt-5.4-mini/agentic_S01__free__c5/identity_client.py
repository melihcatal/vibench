from dataclasses import dataclass
import os
from typing import Dict


@dataclass(frozen=True)
class IdentityConfig:
    base_url: str
    api_key: str
    timeout_seconds: float = 15.0


def build_identity_config() -> IdentityConfig:
    return IdentityConfig(
        base_url=os.environ.get("IDENTITY_API_BASE_URL", "https://api.clerk.com"),
        api_key=os.environ.get("IDENTITY_API_KEY", os.environ.get("CLERK_SECRET_KEY", "")),
        timeout_seconds=float(os.environ.get("IDENTITY_TIMEOUT_SECONDS", "15")),
    )


def identity_base_url(config: IdentityConfig) -> str:
    return config.base_url.rstrip("/")


def build_identity_headers(config: IdentityConfig) -> Dict[str, str]:
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "email-password-account-lifecycle/1.0",
    }
    if config.api_key:
        headers["Authorization"] = f"Bearer {config.api_key}"
    return headers
