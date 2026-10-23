import identity_client


def refresh_session(refresh_token):
    """Refresh an expired session using Auth0 refresh token flow.
    Returns new access token (and optionally ID token) or raises an exception.
    """
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": identity_client.AUTH0_CLIENT_ID,
        "client_secret": identity_client.AUTH0_CLIENT_SECRET,
        "audience": identity_client.AUTH0_AUDIENCE,
    }
    return identity_client.auth0_client.refresh_access_token(payload)
