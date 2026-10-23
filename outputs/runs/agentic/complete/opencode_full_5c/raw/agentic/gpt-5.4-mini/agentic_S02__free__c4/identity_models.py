from dataclasses import dataclass


@dataclass
class TokenResponse:
    access_token: str
    id_token: str | None = None
    refresh_token: str | None = None
    expires_in: int | None = None
    token_type: str | None = None


def parse_token_response(payload):
    return TokenResponse(
        access_token=payload["access_token"],
        id_token=payload.get("id_token"),
        refresh_token=payload.get("refresh_token"),
        expires_in=payload.get("expires_in"),
        token_type=payload.get("token_type"),
    )


def normalize_profile_claims(payload):
    return {
        "subject": payload.get("sub"),
        "email": payload.get("email"),
        "email_verified": bool(payload.get("email_verified")),
        "full_name": payload.get("name") or f"{payload.get('given_name', '')} {payload.get('family_name', '')}".strip(),
        "given_name": payload.get("given_name"),
        "family_name": payload.get("family_name"),
        "picture": payload.get("picture"),
        "locale": payload.get("locale"),
        "provider": "google",
    }
