import base64
import json
import os
from dataclasses import dataclass
from typing import Any
from urllib.parse import urljoin


@dataclass(frozen=True)
class OIDCConfig:
    tenant_id: str
    client_id: str
    client_secret: str
    issuer_base: str
    redirect_uri: str
    scopes: str

    def discovery_url(self) -> str:
        return f"{self.issuer_base.rstrip('/')}/{self.tenant_id}/v2.0/.well-known/openid-configuration"

    def authorization_endpoint(self) -> str:
        return f"{self.issuer_base.rstrip('/')}/{self.tenant_id}/oauth2/v2.0/authorize"

    def token_endpoint(self) -> str:
        return f"{self.issuer_base.rstrip('/')}/{self.tenant_id}/oauth2/v2.0/token"

    def userinfo_endpoint(self) -> str:
        return f"{self.issuer_base.rstrip('/')}/{self.tenant_id}/openid/userinfo"


def build_oidc_config() -> OIDCConfig:
    return OIDCConfig(
        tenant_id=os.environ.get("IDP_TENANT_ID", "common"),
        client_id=os.environ.get("IDP_CLIENT_ID", ""),
        client_secret=os.environ.get("IDP_CLIENT_SECRET", ""),
        issuer_base=os.environ.get("IDP_ISSUER_BASE", "https://login.microsoftonline.com"),
        redirect_uri=os.environ.get("IDP_REDIRECT_URI", "https://example.invalid/callback"),
        scopes=os.environ.get("IDP_SCOPES", "openid profile email offline_access"),
    )


def redirect_uri_for(cfg: OIDCConfig) -> str:
    return cfg.redirect_uri


def build_state_payload(data: dict[str, Any]) -> str:
    raw = json.dumps(data, separators=(",", ":"), sort_keys=True).encode("utf-8")
    return base64.urlsafe_b64encode(raw).rstrip(b"=").decode("ascii")


def verify_state_payload(state: str) -> dict[str, Any]:
    padded = state + "=" * (-len(state) % 4)
    raw = base64.urlsafe_b64decode(padded.encode("ascii"))
    return json.loads(raw.decode("utf-8"))


def normalize_claims_payload(payload: dict[str, Any]) -> dict[str, Any]:
    normalized = dict(payload)
    if "preferred_username" not in normalized and "email" in normalized:
        normalized["preferred_username"] = normalized["email"]
    if "name" not in normalized:
        given = normalized.get("given_name", "")
        family = normalized.get("family_name", "")
        normalized["name"] = " ".join(part for part in [given, family] if part).strip()
    return normalized
