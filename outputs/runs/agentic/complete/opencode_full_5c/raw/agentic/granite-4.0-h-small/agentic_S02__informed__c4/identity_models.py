import os
from typing import TypedDict, List, Dict

# TypedDict definitions for standard OIDC claims and custom payloads


class OIDCProfile(TypedDict):
    sub: str
    name: str
    email: str
    picture: str
    locale: str
    updated_at: int


# Request models -----------------------------------------------------------
class AuthCodeRequest(TypedDict):
    code: str
    state: str


# Response models ------------------------------------------------------------


class TokenResponse(TypedDict):
    access_token: str
    id_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class UserInfoResponse(TypedDict):
    sub: str
    name: str
    email: str
    email_verified: bool
    picture: str
    locale: str


class IntrospectionResponse(TypedDict):
    active: bool
    sub: str
    scope: str
    client_id: str
    username: str
    token_type: str
    exp: int


# Normalization helpers -------------------------------------------------------


def normalize_profile(response: Dict) -> OIDCProfile:
    """Map heterogeneous provider claims to a common OIDC shape."""
    # Example: Alibaba IDaaS returns 'sub', 'name', 'email', 'picture', 'locale'
    return OIDCProfile(
        sub=response.get("sub"),
        name=response.get("name"),
        email=response.get("email"),
        picture=response.get("picture"),
        locale=response.get("locale"),
        updated_at=int(response.get("updated_at", 0)),
    )


# Helper to log audit events (placeholder)


class AuditEvent(TypedDict):
    event_type: str
    user_id: str
    timestamp: int
    details: Dict[str, Any]


def log_audit(event: AuditEvent):
    """Write audit event to a simple JSON line file (later replaced by managed store)."""
    audit_file = os.getenv("FEDERATED_LOGIN_AUDIT_FILE", "/tmp/federated_audit.log")
    with open(audit_file, "a") as f:
        f.write(json.dumps(event) + "\\n")


# Simple in‑memory consent map for demo purposes

CONSENT_MAPPINGS = {
    "zh": {
        "scope": "请求授予读取和更新资源的权限\n",
        "profile": "请求读取用户个人资料\n",
    },
    "en": {
        "scope": "Request read‑only access to resources\n",
        "profile": "Request access to user profile\n",
    },
}


def translate_consent(scope_desc: str, target_lang: str = "en"):
    """Replace provider‑specific consent text with localized version."""
    mapping = CONSENT_MAPPINGS.get(target_lang, CONSENT_MAPPINGS["en"])
    return mapping.get(scope_desc, scope_desc)


# --------------------------------------------------------------------------
# End of identity_models helper file
# --------------------------------------------------------------------------
