from dataclasses import dataclass


@dataclass
class AuthorizationCallback:
    code: str
    state: str
    redirect_uri: str


@dataclass
class TokenResponse:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    token_type: str | None = None
    expires_in: int | None = None


def normalize_profile_claims(claims):
    return {
        "subject": claims.get("sub") or claims.get("user_id") or claims.get("id"),
        "email": claims.get("email"),
        "email_verified": bool(claims.get("email_verified")),
        "name": claims.get("name") or claims.get("preferred_username"),
        "given_name": claims.get("given_name"),
        "family_name": claims.get("family_name"),
        "provider": claims.get("iss") or claims.get("provider") or "cognito",
        "raw": claims,
    }
