from typing import Dict, Any, Optional


class FederatedLoginRequest:
    def __init__(
        self,
        redirect_uri: str,
        scope: str = "openid profile email",
        audience: Optional[str] = None,
    ):
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.audience = audience


class FederatedLoginResponse:
    def __init__(
        self,
        code: Optional[str] = None,
        state: Optional[str] = None,
        error: Optional[str] = None,
        **kwargs,
    ):
        self.code = code
        self.state = state
        self.error = error
        self.raw_response = kwargs


class TokenResponse:
    def __init__(
        self,
        access_token: str,
        id_token: Optional[str] = None,
        token_type: Optional[str] = None,
        expires_in: Optional[int] = None,
        **kwargs,
    ):
        self.access_token = access_token
        self.id_token = id_token
        self.token_type = token_type
        self.expires_in = expires_in
        self.raw_response = kwargs


class UserProfileClaims:
    def __init__(self, claims: Dict[str, Any]):
        self._claims = claims

    def get_claim(self, key: str, default: Any = None) -> Any:
        return self._claims.get(key, default)

    @property
    def sub(self) -> Optional[str]:
        return self.get_claim("sub")

    @property
    def name(self) -> Optional[str]:
        return self.get_claim("name")

    @property
    def email(self) -> Optional[str]:
        return self.get_claim("email")

    @property
    def email_verified(self) -> Optional[bool]:
        return self.get_claim("email_verified")

    def to_dict(self) -> Dict[str, Any]:
        return self._claims


def normalize_auth0_claims(raw_claims: Dict[str, Any]) -> UserProfileClaims:
    # Example of a normalization function from raw Auth0 claims to a standard format
    normalized = {
        "sub": raw_claims.get("sub"),
        "name": raw_claims.get("name"),
        "email": raw_claims.get("email"),
        "email_verified": raw_claims.get("email_verified"),
        "picture": raw_claims.get("picture"),
        "given_name": raw_claims.get("given_name"),
        "family_name": raw_claims.get("family_name"),
        "locale": raw_claims.get("locale"),
    }
    return UserProfileClaims({k: v for k, v in normalized.items() if v is not None})
