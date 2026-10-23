"""Start an OAuth or OIDC authorization-code login using Google Identity Platform."""

import os
from typing import Optional

from identity_client import IdentityClient, GoogleOIDCConfig
from identity_models import AuthRequest


def start_oauth_login(
    prompt: Optional[str] = None,
    scopes: Optional[str] = None,
    state: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> dict:
    """
    Initiate an OAuth/OIDC authorization-code login flow with Google Identity Platform.

    Returns a dict containing the authorization URL, state, and nonce
    for the client to redirect the user to Google's authorization endpoint.
    """
    client = IdentityClient(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scopes=scopes or GoogleOIDCConfig.scopes_str(),
    )

    auth_request = client.create_auth_request(prompt=prompt)

    auth_url = client.build_authorization_url(auth_request)

    return {
        "authorization_url": auth_url,
        "state": auth_request.state,
        "nonce": auth_request.nonce,
        "provider": GoogleOIDCConfig.PROVIDER_NAME,
        "authorization_endpoint": GoogleOIDCConfig.AUTHORIZATION_ENDPOINT,
        "scopes": client.scopes,
    }


if __name__ == "__main__":
    result = start_oauth_login()
    print("Authorization URL:", result["authorization_url"])
    print("State:", result["state"])
