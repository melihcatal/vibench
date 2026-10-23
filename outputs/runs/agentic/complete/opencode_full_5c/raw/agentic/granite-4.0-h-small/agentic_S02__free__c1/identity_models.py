# identity_models.py
# [HELPER] Define local request, response, and normalization helpers for Federated Login Flow

from typing import Any, Dict, List, Optional


class NormalizedClaims:
    def __init__(
        self,
        user_id: str,
        email: Optional[str] = None,
        full_name: Optional[str] = None,
        given_name: Optional[str] = None,
        family_name: Optional[str] = None,
        picture_url: Optional[str] = None,
        locale: Optional[str] = None,
        extra: Optional[Dict[str, Any]] = None,
    ):
        self.user_id = user_id
        self.email = email
        self.full_name = full_name
        self.given_name = given_name
        self.family_name = family_name
        self.picture_url = picture_url
        self.locale = locale
        self.extra = extra or {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "full_name": self.full_name,
            "given_name": self.given_name,
            "family_name": self.family_name,
            "picture_url": self.picture_url,
            "locale": self.locale,
            **self.extra,
        }


class AuthRequest:
    def __init__(self, client_id: str, redirect_uri: str, scopes: List[str], state: str, code_challenge: Optional[str] = None, challenge_method: Optional[str] = None):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.state = state
        self.code_challenge = code_challenge
        self.challenge_method = challenge_method

    def as_query_string(self) -> str:
        qs = {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": "code",
            "scope": " ".join(self.scopes),
            "state": self.state,
        }
        if self.code_challenge:
            qs["code_challenge"] = self.code_challenge
        if self.challenge_method:
            qs["code_challenge_method"] = self.challenge_method
        return urllib.parse.urlencode(qs)


class TokenResponse:
    def __init__(self, access_token: str, refresh_token: Optional[str] = None, id_token: Optional[str] = None, expires_in: Optional[int] = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.id_token = id_token
        self.expires_in = expires_in

    @property
    def expires_at(self) -> Optional[int]:
        if self.expires_in is not None:
            return int(time.time()) + self.expires_in
        return None

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "access_token": self.access_token,
            "expires_in": self.expires_in,
        }
        if self.refresh_token:
            d["refresh_token"] = self.refresh_token
        if self.id_token:
            d["id_token"] = self.id_token
        return d


class ProfileRequest:
    def __init__(self, provider: str, user_id: str):
        self.provider = provider
        self.user_id = user_id

    # Additional provider‑specific methods could be added later


class ProfileResponse:
    def __init__(self, raw_json: Dict[str, Any]):
        self.raw = raw_json
        # Normalized fields can be derived by ProfileResponse.normalize() implementations

    def normalize(self) -> NormalizedClaims:
        """Convert provider‑specific payload to a consistent claim set."""
        # Override in provider‑specific subclasses if needed
        raise NotImplementedError("Subclasses must implement normalize")


class ProviderError(Exception):
    def __init__(self, provider: str, message: str):
        self.provider = provider
        self.message = message
        super().__init__(f"{provider}: {message}")

# Utility imports used throughout the package
import urllib.parse
import time

# Example helper to validate a JWT (not called directly here but useful for other modules)
import jwt

 def decode_jwt(token: str, verify: bool = False, key: Optional[str] = None) -> Dict[str, Any]:
    try:
        payload = jwt.decode(token, key=key, verify=verify, options={"require": []})
        return payload
    except jwt.PyJWKClientError as e:
        raise ValueError(f"Invalid JWT: {e}")
