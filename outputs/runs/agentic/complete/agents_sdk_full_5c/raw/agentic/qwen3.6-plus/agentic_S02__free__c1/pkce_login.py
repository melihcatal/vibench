"""
Implement a PKCE (Proof Key for Code Exchange) login flow for public
clients using Auth0.

PKCE is required for public clients (SPAs, mobile apps) to prevent
authorization code interception attacks. This module generates the
code verifier and code challenge, builds the Auth0 authorization URL,
and handles the token exchange with code_verifier.
"""

import os
from typing import Any, Dict, Optional

from identity_models import (
    OAuthAuthorizationRequest,
    TokenResponse,
    generate_code_verifier,
    generate_code_challenge,
    generate_state,
    generate_nonce,
)
from identity_client import (
    IdentityClient,
    AUTH0_AUTHORIZE_URL,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
)


class PKCELoginSession:
    """
    Manages a PKCE login session for Auth0.

    Holds the code verifier, code challenge, state, and nonce for a
    single login attempt. The code verifier must be kept secret and
    passed to the token exchange step.

    Auth0 supports PKCE with S256 code challenge method for all
    application types including confidential and public clients.
    """

    def __init__(
        self,
        code_verifier: Optional[str] = None,
        state: Optional[str] = None,
        nonce: Optional[str] = None,
    ):
        self.code_verifier = code_verifier or generate_code_verifier()
        self.code_challenge = generate_code_challenge(self.code_verifier)
        self.state = state or generate_state()
        self.nonce = nonce or generate_nonce()
        self.code_challenge_method = "S256"

    def build_authorization_url(
        self,
        client_id: Optional[str] = None,
        redirect_uri: Optional[str] = None,
        scope: str = "openid profile email",
        audience: Optional[str] = None,
        connection: Optional[str] = None,
        prompt: Optional[str] = None,
    ) -> str:
        """
        Build the Auth0 /authorize URL with PKCE parameters.

        The code_challenge and code_challenge_method=S256 are appended
        to the authorization request as required by RFC 7636. Auth0
        validates the code_verifier at the token endpoint.
        """
        cid = client_id or AUTH0_CLIENT_ID
        ruri = redirect_uri or AUTH0_REDIRECT_URI
        aud = audience or os.environ.get("AUTH0_AUDIENCE")

        request = OAuthAuthorizationRequest(
            client_id=cid,
            redirect_uri=ruri,
            response_type="code",
            scope=scope,
            state=self.state,
            nonce=self.nonce,
            audience=aud,
            connection=connection,
            prompt=prompt,
            code_challenge=self.code_challenge,
            code_challenge_method=self.code_challenge_method,
        )

        return request.to_url(AUTH0_AUTHORIZE_URL)

    def exchange_code_for_tokens(
        self,
        code: str,
        client: Optional[IdentityClient] = None,
    ) -> TokenResponse:
        """
        Exchange the authorization code for tokens at the Auth0
        /oauth/token endpoint, including the code_verifier.

        Auth0 requires the code_verifier to match the code_challenge
        sent during authorization. If they don't match, Auth0 returns
        an invalid_grant error.
        """
        if client is None:
            client = IdentityClient()

        token_data = client.exchange_authorization_code(
            code=code,
            code_verifier=self.code_verifier,
        )

        from identity_models import extract_id_token_claims

        id_token_claims = {}
        id_token_raw = token_data.get("id_token")
        if id_token_raw:
            id_token_claims = extract_id_token_claims(id_token_raw)

        return TokenResponse(
            access_token=token_data["access_token"],
            token_type=token_data.get("token_type", "Bearer"),
            expires_in=token_data.get("expires_in", 3600),
            id_token=id_token_raw,
            refresh_token=token_data.get("refresh_token"),
            scope=token_data.get("scope"),
            raw_response=token_data,
        )

    def to_dict(self) -> Dict[str, str]:
        """Serialize session data for storage (e.g., in a cookie or session)."""
        return {
            "code_verifier": self.code_verifier,
            "code_challenge": self.code_challenge,
            "state": self.state,
            "nonce": self.nonce,
            "code_challenge_method": self.code_challenge_method,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, str]) -> "PKCELoginSession":
        """Reconstruct a PKCE session from stored data."""
        session = cls(
            code_verifier=data["code_verifier"],
            state=data.get("state"),
            nonce=data.get("nonce"),
        )
        return session


def initiate_pkce_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: str = "openid profile email",
    audience: Optional[str] = None,
    connection: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Initiate a full PKCE login flow with Auth0.

    Creates a new PKCELoginSession, generates the authorization URL,
    and returns the URL along with session data that must be stored
    for callback verification.

    This is the recommended approach for public clients (SPAs, mobile)
    where client_secret cannot be securely stored.
    """
    session = PKCELoginSession()

    authorize_url = session.build_authorization_url(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope=scope,
        audience=audience,
        connection=connection,
    )

    return {
        "authorize_url": authorize_url,
        "session": session.to_dict(),
        "auth0_domain": os.environ.get("AUTH0_DOMAIN", "dev-example.us.auth0.com"),
        "code_challenge_method": "S256",
    }


def complete_pkce_callback(
    query_params: Dict[str, str],
    session_data: Dict[str, str],
    client: Optional[IdentityClient] = None,
) -> TokenResponse:
    """
    Complete a PKCE login by processing the Auth0 callback.

    Validates the state parameter and exchanges the authorization code
    with the stored code_verifier.
    """
    session = PKCELoginSession.from_dict(session_data)

    from oauth_callback import handle_oauth_callback

    return handle_oauth_callback(
        query_params=query_params,
        expected_state=session.state,
        code_verifier=session.code_verifier,
        client=client,
    )


if __name__ == "__main__":
    result = initiate_pkce_login()
    print(f"PKCE Authorize URL: {result['authorize_url']}")
    print(f"Code Challenge Method: {result['code_challenge_method']}")
    print(f"State: {result['session']['state']}")
