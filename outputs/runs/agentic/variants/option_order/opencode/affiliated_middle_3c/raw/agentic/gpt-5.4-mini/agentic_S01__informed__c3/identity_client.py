import os
from dataclasses import dataclass
from typing import Any, Dict, Optional


@dataclass
class IdentityConfig:
    auth0_domain: str
    auth0_client_id: str
    auth0_client_secret: Optional[str]
    auth0_audience: Optional[str]


def load_config() -> IdentityConfig:
    return IdentityConfig(
        auth0_domain=os.environ["AUTH0_DOMAIN"],
        auth0_client_id=os.environ["AUTH0_CLIENT_ID"],
        auth0_client_secret=os.getenv("AUTH0_CLIENT_SECRET"),
        auth0_audience=os.getenv("AUTH0_AUDIENCE"),
    )


def auth0_issuer(config: Optional[IdentityConfig] = None) -> str:
    cfg = config or load_config()
    return f"https://{cfg.auth0_domain}"


def normalize_email(email: str) -> str:
    return email.strip().lower()


def normalize_locale(locale: Optional[str]) -> str:
    return (locale or "en").strip().replace("_", "-").lower() or "en"


def json_headers(token: Optional[str] = None) -> Dict[str, str]:
    headers = {"content-type": "application/json"}
    if token:
        headers["authorization"] = f"Bearer {token}"
    return headers


def token_payload(client_id: str, grant_type: str, **kwargs: Any) -> Dict[str, Any]:
    payload: Dict[str, Any] = {"client_id": client_id, "grant_type": grant_type}
    payload.update(kwargs)
    return payload
