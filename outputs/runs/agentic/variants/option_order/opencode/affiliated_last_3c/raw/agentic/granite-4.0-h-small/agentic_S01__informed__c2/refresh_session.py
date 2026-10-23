# [SAME-SCENARIO] refresh_session.py
# Refresh an expired session or access token using Auth0 Management API

import os
from auth0.v3.authentication import Tokens

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

tokens = Tokens(AUTH0_DOMAIN, AUTH0_CLIENT_ID)


def refresh_session(refresh_token):
    """Exchange a refresh token for a new access token.

    Returns the new access_token on success, raises on failure.
    """
    new_token = tokens.refresh_token(refresh_token=refresh_token)
    return new_token["access_token"]
