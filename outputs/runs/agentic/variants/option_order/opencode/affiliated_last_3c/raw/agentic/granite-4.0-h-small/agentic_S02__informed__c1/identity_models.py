from typing import Dict, Any

# Simple request/response model for the federated login flow


class LoginRequest:
    """Encapsulates data needed to start an OIDC/OAuth login.

    Attributes reflect common provider configuration variables.
    """

    def __init__(
        self,
        domain: str,
        client_id: str,
        redirect_uri: str,
        scopes: str = "openid profile email",
    ):
        self.domain = domain
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes

    def as_dict(self) -> Dict[str, Any]:
        return {
            "domain": self.domain,
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "scopes": self.scopes,
        }


class TokenResponse:
    """Model the token exchange response from an identity provider.

    Include fields commonly returned by OIDC and OAuth2 providers.
    """

    def __init__(
        self,
        id_token: str = None,
        access_token: str = None,
        refresh_token: str = None,
        expires_in: int = None,
    ):
        self.id_token = id_token
        self.access_token = access_token
        self.refresh_token = refresh_token
        self.expires_in = expires_in

    def is_valid(self) -> bool:
        return self.id_token or self.access_token

    def as_dict(self) -> Dict[str, Any]:
        return {
            "id_token": self.id_token,
            "access_token": self.access_token,
            "refresh_token": self.refresh_token,
            "expires_in": self.expires_in,
        }


# Normalized profile shape used by the profile_claims module
UserProfile = Dict[str, Any]
