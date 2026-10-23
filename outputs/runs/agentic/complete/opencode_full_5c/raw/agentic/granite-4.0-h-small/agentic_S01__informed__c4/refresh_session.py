from identity_client import IdentityClient

# SAME-SCENARIO: Refresh an access token or session


def refresh_session(refresh_token: str, client: IdentityClient):
    """Refresh an expired session or access token using a refresh token.

    Args:
        refresh_token: Token issued to refresh an access token.
        client: IdentityClient configured with the target provider.

    Returns:
        dict: New access token and optional ID token.
    """
    payload = client.build_refresh_payload(refresh_token=refresh_token)
    response = client.call_api("POST", "/token/refresh", json=payload)
    client.validate_response(response, "refresh")
    return response.json()
