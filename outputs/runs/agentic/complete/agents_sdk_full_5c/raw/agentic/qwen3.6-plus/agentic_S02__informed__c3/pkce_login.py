"""Implement a PKCE login flow for public clients using Google Identity Platform OIDC."""

import os
import time
from typing import Optional, Dict, Any

import requests

from identity_client import IdentityClient, GoogleOIDCConfig
from identity_models import (
    AuthRequest,
    TokenExchangeRequest,
    TokenResponse,
    generate_pkce_pair,
    generate_state,
    UserProfileClaims,
)


def start_pkce_login(
    scopes: Optional[str] = None,
    prompt: Optional[str] = None,
    client_id: Optional[str] = None,
    redirect_uri: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Initiate a PKCE (Proof Key for Code Exchange) login flow.
    Returns the authorization URL along with the state and code_verifier
    that must be stored securely for the callback step.
    """
    client = IdentityClient(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scopes=scopes or GoogleOIDCConfig.scopes_str(),
    )

    auth_request, pkce_data = client.create_pkce_auth_request(prompt=prompt)
    auth_url = client.build_authorization_url(auth_request)

    return {
        "authorization_url": auth_url,
        "state": auth_request.state,
        "nonce": auth_request.nonce,
        "code_verifier": pkce_data["code_verifier"],
        "code_challenge": pkce_data["code_challenge"],
        "code_challenge_method": "S256",
        "provider": GoogleOIDCConfig.PROVIDER_NAME,
    }


def complete_pkce_login(
    authorization_code: str,
    code_verifier: str,
    state_received: Optional[str] = None,
    state_expected: Optional[str] = None,
    redirect_uri: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Complete the PKCE login by exchanging the authorization code for tokens.
    """
    if state_expected and state_received:
        if state_received != state_expected:
            return {
                "error": "state_mismatch",
                "message": "OAuth state validation failed",
                "provider": GoogleOIDCConfig.PROVIDER_NAME,
            }

    token_request = TokenExchangeRequest(
        code=authorization_code,
        redirect_uri=redirect_uri,
        client_id=client_id,
        code_verifier=code_verifier,
    )

    body = token_request.to_form_body()

    try:
        response = requests.post(
            GoogleOIDCConfig.TOKEN_ENDPOINT,
            data=body,
            headers={"Accept": "application/json"},
            timeout=30,
        )
        response.raise_for_status()
        token_data = response.json()

        token_response = TokenResponse.from_dict(token_data)

        result = {
            "success": True,
            "token_type": token_response.token_type,
            "access_token": token_response.access_token,
            "expires_in": token_response.expires_in,
            "scope": token_response.scope,
            "has_id_token": token_response.id_token is not None,
            "provider": GoogleOIDCConfig.PROVIDER_NAME,
            "timestamp": time.time(),
        }

        if token_response.id_token:
            result["id_token"] = token_response.id_token

        return result

    except requests.RequestException as exc:
        return {
            "success": False,
            "error": "token_exchange_failed",
            "message": str(exc),
            "provider": GoogleOIDCConfig.PROVIDER_NAME,
        }


def full_pkce_flow(
    authorization_code: str,
    code_verifier: str,
    state_received: Optional[str] = None,
    state_expected: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Execute the complete PKCE flow from code exchange through profile fetch.
    """
    exchange_result = complete_pkce_login(
        authorization_code=authorization_code,
        code_verifier=code_verifier,
        state_received=state_received,
        state_expected=state_expected,
    )

    if not exchange_result.get("success"):
        return exchange_result

    access_token = exchange_result.get("access_token", "")
    if not access_token:
        return {
            "error": "no_access_token",
            "message": "No access token returned in exchange",
            "provider": GoogleOIDCConfig.PROVIDER_NAME,
        }

    from profile_claims import fetch_and_normalize_profile

    profile_result = fetch_and_normalize_profile(
        access_token=access_token,
        id_token=exchange_result.get("id_token"),
    )

    return {
        "tokens": exchange_result,
        "profile": profile_result,
        "provider": GoogleOIDCConfig.PROVIDER_NAME,
    }


if __name__ == "__main__":
    login_data = start_pkce_login()
    print("PKCE Authorization URL:", login_data["authorization_url"])
    print("Store code_verifier securely:", login_data["code_verifier"])
