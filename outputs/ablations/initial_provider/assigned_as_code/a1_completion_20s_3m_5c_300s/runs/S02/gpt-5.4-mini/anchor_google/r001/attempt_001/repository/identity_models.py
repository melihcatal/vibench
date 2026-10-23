from dataclasses import dataclass


def normalize_claims(claims):
    result = {}
    for key, value in (claims or {}).items():
        if value is None:
            continue
        if key in {"email_verified", "verified_email"}:
            result[key] = bool(value)
        elif key in {"iat", "exp", "auth_time"}:
            result[key] = int(value)
        else:
            result[key] = value
    if "sub" in result and "user_id" not in result:
        result["user_id"] = result["sub"]
    if "name" not in result and "given_name" in result and "family_name" in result:
        result["name"] = f"{result['given_name']} {result['family_name']}".strip()
    return result


@dataclass
class TokenBundle:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None


@dataclass
class LoginRequest:
    redirect_uri: str
    provider_id: str
    tenant_id: str | None = None
    code_verifier: str | None = None
