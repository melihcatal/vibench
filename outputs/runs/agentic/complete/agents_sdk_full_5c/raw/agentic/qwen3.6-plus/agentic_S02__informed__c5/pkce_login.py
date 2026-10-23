"""Implement a PKCE login flow for public clients with Auth0.

This module implements the full Proof Key for Code Exchange (PKCE)
authorization-code flow for public clients using Auth0.

Provider: Auth0 Authentication API
SDK: requests / OIDC protocol
Auth env vars: AUTH0_DOMAIN, AUTH0_CLIENT_ID
"""

import os
import requests
from typing import Optional, Dict, Any

from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_CALLBACK_URL,
    AUTH0_AUTHORIZATION_ENDPOINT,
    AUTH0_TOKEN_ENDPOINT,
    AUTH0_SCOPE,
    generate_state,
    generate_code_verifier,
    generate_code_challenge,
    validate_state,
)
from identity_models import TokenResponse, UserProfile


def initiate_pkce_login(
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    scope: Optional[str] = None,
    audience: Optional[str] = None,
    code_verifier: Optional[str] = None,
) -> dict:
    """Initiate a PKCE authorization-code login with Auth0.

    Generates the PKCE code verifier and challenge, then builds
    the Auth0 authorization URL.

    Args:
        client_id: Auth0 Client ID for public client.
        redirect_uri: Callback URL after authentication.
        scope: OIDC scopes to request.
        audience: Auth0 API audience identifier.
        code_verifier: Optional pre-generated code verifier.

    Returns:
        dict with 'authorization_url', 'state', and 'code_verifier'.
    """
    state = generate_state()
    verifier = code_verifier or generate_code_verifier()
    challenge = generate_code_challenge(verifier)

    params = {
        "client_id": client_id or AUTH0_CLIENT_ID or "",
        "redirect_uri": redirect_uri or AUTH0_CALLBACK_URL,
        "scope": scope or AUTH0_SCOPE,
        "response_type": "code",
        "code_challenge": challenge,
        "code_challenge_method": "S256",
        "state": state,
    }

    if audience:
        params["audience"] = audience

    query_string = "&".join(f"{k}={v}" for k, v in params.items())
    auth_url = f"{AUTH0_AUTHORIZATION_ENDPOINT}?{query_string}"

    return {
        "authorization_url": auth_url,
        "state": state,
        "code_verifier": verifier,
        "provider": "Auth0",
    }


def complete_pkce_login(
    authorization_code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> TokenResponse:
    """Complete the PKCE login by exchanging the code for tokens with Auth0.

    Args:
        authorization_code: The authorization code from Auth0 callback.
        state: The state parameter from the callback.
        expected_state: The original state from initiation.
        code_verifier: The original code verifier.
        client_id: Auth0 Client ID.
        redirect_uri: The redirect URI used in initiation.

    Returns:
        TokenResponse with the exchanged tokens.

    Raises:
        ValueError: If state validation fails.
        requests.RequestException: If the token exchange fails.
    """
    if not validate_state(state, expected_state):
        raise ValueError("PKCE state validation failed")

    token_data = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": redirect_uri or AUTH0_CALLBACK_URL,
        "client_id": client_id or AUTH0_CLIENT_ID or "",
        "code_verifier": code_verifier,
    }

    headers = {"Content-Type": "application/x-www-form-urlencoded"}

    response = requests.post(
        AUTH0_TOKEN_ENDPOINT,
        data=token_data,
        headers=headers,
        timeout=30,
    )
    response.raise_for_status()

    return TokenResponse.from_auth0_response(response.json())


def full_pkce_flow(
    authorization_code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    fetch_profile: bool = False,
) -> Dict[str, Any]:
    """Execute the full PKCE flow and optionally fetch the user profile.

    Args:
        authorization_code: Auth0 authorization code.
        state: State from callback.
        expected_state: Original state.
        code_verifier: PKCE code verifier.
        fetch_profile: Whether to fetch the user profile after login.

    Returns:
        dict with tokens and optionally user profile.
    """
    tokens = complete_pkce_login(
        authorization_code=authorization_code,
        state=state,
        expected_state=expected_state,
        code_verifier=code_verifier,
    )

    result: Dict[str, Any] = {
        "tokens": tokens,
        "provider": "Auth0",
    }

    if fetch_profile and tokens.access_token:
        from identity_client import AUTH0_USERINFO_ENDPOINT
        userinfo_resp = requests.get(
            AUTH0_USERINFO_ENDPOINT,
            headers={"Authorization": f"Bearer {tokens.access_token}"},
            timeout=30,
        )
        userinfo_resp.raise_for_status()
        result["profile"] = UserProfile.from_auth0_userinfo(userinfo_resp.json())

    return result


if __name__ == "__main__":
    login = initiate_pkce_login()
    print(f"PKCE Authorization URL: {login['authorization_url']}")
    print(f"Code Verifier (store securely): {login['code_verifier']}")
