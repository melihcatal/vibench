"""
Implement a PKCE (Proof Key for Code Exchange) login flow for public clients.
Follows RFC 7636 with Auth0 as the identity provider.
"""

import os
import asyncio
import secrets
from typing import Optional, Dict, Any

from identity_client import (
    create_auth0_client,
    generate_state,
    generate_code_verifier,
    generate_code_challenge,
    AUTH0_DOMAIN,
    AUTH0_CLIENT_ID,
    AUTH0_REDIRECT_URI,
)
from identity_models import TokenResponse, redact_sensitive_fields


class PKCELoginError(Exception):
    """Raised when the PKCE login flow encounters an error."""
    pass


def initiate_pkce_flow(
    scope: str = "openid profile email",
    redirect_uri: Optional[str] = None,
    audience: Optional[str] = None,
    connection: Optional[str] = None,
    code_verifier: Optional[str] = None,
    state: Optional[str] = None,
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Initiate a PKCE authorization flow with Auth0.

    Generates code verifier/challenge pair and constructs the authorization URL.
    """
    verifier = code_verifier or generate_code_verifier()
    challenge = generate_code_challenge(verifier)
    login_state = state or generate_state()

    client = create_auth0_client(
        domain=domain or os.getenv("AUTH0_DOMAIN", AUTH0_DOMAIN),
        client_id=client_id or os.getenv("AUTH0_CLIENT_ID", AUTH0_CLIENT_ID),
        redirect_uri=redirect_uri or os.getenv("AUTH0_REDIRECT_URI", AUTH0_REDIRECT_URI),
        audience=audience or os.getenv("AUTH0_AUDIENCE"),
    )

    extra_params = {
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    if connection:
        extra_params["connection"] = connection

    auth_url = client.authorize_url(
        state=login_state,
        scope=scope,
        response_type="code",
        extra_params=extra_params,
    )

    return {
        "authorization_url": auth_url,
        "state": login_state,
        "code_verifier": verifier,
        "code_challenge": challenge,
        "session_data": {
            "state": login_state,
            "code_verifier": verifier,
            "redirect_uri": client.redirect_uri,
            "scope": scope,
            "auth0_domain": client.domain,
            "auth0_client_id": client.client_id,
            "pkce_method": "S256",
        },
    }


async def complete_pkce_exchange(
    code: str,
    state: str,
    expected_state: str,
    code_verifier: str,
    redirect_uri: Optional[str] = None,
    domain: Optional[str] = None,
    client_id: Optional[str] = None,
    client_secret: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Complete the PKCE flow by exchanging the authorization code for tokens.

    Includes the code_verifier in the token request per RFC 7636.
    """
    if state != expected_state:
        raise PKCELoginError(
            f"PKCE state mismatch: expected {expected_state}, got {state}"
        )

    client = create_auth0_client(
        domain=domain or os.getenv("AUTH0_DOMAIN", AUTH0_DOMAIN),
        client_id=client_id or os.getenv("AUTH0_CLIENT_ID", AUTH0_CLIENT_ID),
        client_secret=client_secret or os.getenv("AUTH0_CLIENT_SECRET", ""),
        redirect_uri=redirect_uri or os.getenv("AUTH0_REDIRECT_URI"),
    )

    try:
        token_data = await client.exchange_code(code, code_verifier=code_verifier)
    except Exception as exc:
        raise PKCELoginError(f"PKCE token exchange failed: {exc}") from exc

    if "error" in token_data:
        raise PKCELoginError(
            f"Auth0 PKCE error: {token_data.get('error')} - {token_data.get('error_description', '')}"
        )

    tokens = TokenResponse.from_auth0_response(token_data)

    return {
        "tokens": tokens,
        "token_data": redact_sensitive_fields(token_data),
        "provider": "auth0",
        "pkce_method": "S256",
        "domain": client.domain,
    }


async def full_pkce_login(
    authorization_code: str,
    session_data: Dict[str, Any],
    callback_state: str,
) -> Dict[str, Any]:
    """
    Execute the full PKCE login flow: validate callback state and exchange code.
    """
    expected_state = session_data.get("state")
    code_verifier = session_data.get("code_verifier")
    redirect_uri = session_data.get("redirect_uri")

    if not code_verifier:
        raise PKCELoginError("Missing code_verifier in session data")

    return await complete_pkce_exchange(
        code=authorization_code,
        state=callback_state,
        expected_state=expected_state,
        code_verifier=code_verifier,
        redirect_uri=redirect_uri,
    )


def generate_pkce_session_key() -> str:
    """Generate a session key for storing PKCE state server-side."""
    return f"pkce_{secrets.token_hex(16)}"


if __name__ == "__main__":
    async def main():
        flow = initiate_pkce_flow()
        print(f"PKCE Auth URL: {flow['authorization_url']}")
        print(f"Code Challenge: {flow['code_challenge']}")
        print(f"PKCE Method: S256")

    asyncio.run(main())
