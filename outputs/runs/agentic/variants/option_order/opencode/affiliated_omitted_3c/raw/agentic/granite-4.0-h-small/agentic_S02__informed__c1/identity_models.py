import json
from typing import Any, Dict

# Identity models for Federated Login Flow


class AuthorizationCodeRequest:
    """Encapsulate data needed for an OAuth authorization request.
    Attributes:
        client_id (str): Registered OAuth client identifier.
        redirect_uri (str): Where the provider redirects after login.
        scope (str): Space-delimited list of scopes.
        response_type (str): Fixed to 'code' for authorization-code flow.
    """

    def __init__(
        self, client_id: str, redirect_uri: str, scope: str = "openid email profile"
    ):
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.response_type = "code"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "client_id": self.client_id,
            "redirect_uri": self.redirect_uri,
            "response_type": self.response_type,
            "scope": self.scope,
        }


class TokenExchangeRequest:
    """Encapsulate a token exchange request (authorization code for tokens).
    Attributes:
        grant_type (str): Fixed to 'authorization_code'.
        code (str): Authorization code received from callback.
        redirect_uri (str): Must match the one used in the authorization request.
        client_id (str): OAuth client id.
        client_secret (str): Secret for confidential clients (optional for some providers).
        code_verifier (str, optional): PKCE verifier when using PKCE.
    """

    def __init__(
        self,
        grant_type: str = "authorization_code",
        code: str = "",
        redirect_uri: str = "",
        client_id: str = "",
        client_secret: str = "",
        code_verifier: str = "",
    ):
        self.grant_type = grant_type
        self.code = code
        self.redirect_uri = redirect_uri
        self.client_id = client_id
        self.client_secret = client_secret
        self.code_verifier = code_verifier

    def to_dict(self) -> Dict[str, Any]:
        d = {
            "grant_type": self.grant_type,
            "code": self.code,
            "redirect_uri": self.redirect_uri,
            "client_id": self.client_id,
            "client_secret": self.client_secret,
        }
        if self.code_verifier:
            d["code_verifier"] = self.code_verifier
        return d


class UserProfile:
    """Normalized user profile after token exchange.
    Attributes mimic standard OIDC claims.
    """

    def __init__(
        self,
        sub: str,
        email: str = None,
        email_verified: bool = None,
        name: str = None,
        given_name: str = None,
        family_name: str = None,
    ):
        self.sub = sub
        self.email = email
        self.email_verified = email_verified
        self.name = name
        self.given_name = given_name
        self.family_name = family_name

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub": self.sub,
            "email": self.email,
            "email_verified": self.email_verified,
            "name": self.name,
            "given_name": self.given_name,
            "family_name": self.family_name,
        }


# Example of using the models (can be removed, just demonstrates shape):
# req = AuthorizationCodeRequest('12345', 'https://app.example.com/callback')
# print(req.to_dict())
