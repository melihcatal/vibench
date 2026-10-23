from typing import TypedDict, Dict, Any


class ProfileClaims(TypedDict):
    sub: str
    email: str
    name: str
    picture: str


class TokenResponse(TypedDict):
    access_token: str
    id_token: str
    token_type: str
    expires_in: int


class UserInfoResponse(TypedDict):
    sub: str
    email: str
    name: str
    picture: str


def normalize_claims(raw_claims: Dict[str, Any]) -> ProfileClaims:
    """Normalize federated profile claims to internal schema."""
    # Example normalization logic for Okta/Azure/Google
    normalized: ProfileClaims = {
        "sub": raw_claims.get("sub") or raw_claims.get("sub") or "unknown-sub",
        "email": raw_claims.get("email") or raw_claims.get("email"),
        "name": raw_claims.get("name") or raw_claims.get("name"),
        "picture": raw_claims.get("picture") or raw_claims.get("picture"),
    }
    return normalized


def validate_token(token: TokenResponse) -> bool:
    """Simple validation - checks required fields are present."""
    required = ["access_token", "id_token", "token_type", "expires_in"]
    return all(k in token for k in required)
