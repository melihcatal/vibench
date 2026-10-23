import json
from typing import Dict, Any, Optional

class FederatedLoginRequest:
    """
    Represents a request for initiating a federated login.
    """
    def __init__(self, redirect_uri: str, state: str, scope: str = "openid profile email", pkce_code_challenge: Optional[str] = None, pkce_code_challenge_method: Optional[str] = None):
        self.redirect_uri = redirect_uri
        self.state = state
        self.scope = scope
        self.pkce_code_challenge = pkce_code_challenge
        self.pkce_code_challenge_method = pkce_code_challenge_method

    def to_dict(self) -> Dict[str, Any]:
        data = {
            "redirect_uri": self.redirect_uri,
            "state": self.state,
            "scope": self.scope,
        }
        if self.pkce_code_challenge and self.pkce_code_challenge_method:
            data["pkce_code_challenge"] = self.pkce_code_challenge
            data["pkce_code_challenge_method"] = self.pkce_code_challenge_method
        return data

class OAuthTokenResponse:
    """
    Represents the response from an OAuth token endpoint.
    """
    def __init__(self, access_token: str, id_token: Optional[str] = None, expires_in: Optional[int] = None, token_type: str = "Bearer", refresh_token: Optional[str] = None):
        self.access_token = access_token
        self.id_token = id_token
        self.expires_in = expires_in
        self.token_type = token_type
        self.refresh_token = refresh_token

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls(
            access_token=data.get("access_token"),
            id_token=data.get("id_token"),
            expires_in=data.get("expires_in"),
            token_type=data.get("token_type", "Bearer"),
            refresh_token=data.get("refresh_token"),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "access_token": self.access_token,
            "id_token": self.id_token,
            "expires_in": self.expires_in,
            "token_type": self.token_type,
            "refresh_token": self.refresh_token,
        }

class NormalizedUserProfile:
    """
    Represents a normalized user profile, abstracting away provider-specific claim names.
    """
    def __init__(
        self,
        user_id: str,
        email: Optional[str] = None,
        display_name: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        avatar_url: Optional[str] = None,
        raw_claims: Optional[Dict[str, Any]] = None,
    ):
        self.user_id = user_id
        self.email = email
        self.display_name = display_name
        self.first_name = first_name
        self.last_name = last_name
        self.avatar_url = avatar_url
        self.raw_claims = raw_claims if raw_claims is not None else {}

    def to_dict(self) -> Dict[str, Any]:
        return {
            "user_id": self.user_id,
            "email": self.email,
            "display_name": self.display_name,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "avatar_url": self.avatar_url,
            "raw_claims": self.raw_claims,
        }

    @classmethod
    def from_raw_claims(cls, claims: Dict[str, Any]):
        """
        Normalizes raw claims from an identity provider into a common profile structure.
        Assumes Auth0-like claim names, but can be adapted.
        """
        return cls(
            user_id=claims.get("sub") or claims.get("user_id"),
            email=claims.get("email"),
            display_name=claims.get("name") or claims.get("preferred_username") or claims.get("email"),
            first_name=claims.get("given_name"),
            last_name=claims.get("family_name"),
            avatar_url=claims.get("picture"),
            raw_claims=claims,
        )

if __name__ == '__main__':
    # Example Usage
    print("--- FederatedLoginRequest ---")
    login_req = FederatedLoginRequest(
        redirect_uri="http://localhost:5000/callback",
        state="abc123xyz",
        pkce_code_challenge="some_challenge",
        pkce_code_challenge_method="S256",
    )
    print(json.dumps(login_req.to_dict(), indent=2))

    print("\n--- OAuthTokenResponse ---")
    token_data = {
        "access_token": "ey...",
        "id_token": "ey...",
        "expires_in": 3600,
        "token_type": "Bearer",
        "refresh_token": "rt_ey...",
    }
    token_resp = OAuthTokenResponse.from_dict(token_data)
    print(json.dumps(token_resp.to_dict(), indent=2))

    print("\n--- NormalizedUserProfile ---")
    raw_auth0_claims = {
        "sub": "auth0|12345",
        "nickname": "testuser",
        "name": "Test User",
        "picture": "https://example.com/avatar.png",
        "email": "test@example.com",
        "given_name": "Test",
        "family_name": "User",
        "locale": "en-US",
    }
    normalized_profile = NormalizedUserProfile.from_raw_claims(raw_auth0_claims)
    print(json.dumps(normalized_profile.to_dict(), indent=2))
