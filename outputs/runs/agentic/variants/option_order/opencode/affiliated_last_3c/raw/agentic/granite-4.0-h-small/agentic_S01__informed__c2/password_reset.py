# [SAME-SCENARIO] password_reset.py
# Start a password reset flow for a local account using Auth0 Management API

import os
from auth0.v3.management import Users

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")

users = Users(AUTH0_DOMAIN)


def start_password_reset(email, connection="Username-Password-Authentication"):
    """Trigger a password reset email for the given email address.

    Returns None on success, raises on failure.
    """
    return users.change_password(email=email, connection=connection)
