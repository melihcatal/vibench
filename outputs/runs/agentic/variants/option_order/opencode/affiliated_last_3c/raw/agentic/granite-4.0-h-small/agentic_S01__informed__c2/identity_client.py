# [HELPER] identity_client.py
# Local configuration and client helper utilities for Email/Password Account Lifecycle

import os
from auth0.v3.management import UserManagement
from auth0.v3.authentication import Users, Tokens

# ----- Provider configuration ----- #
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

# ----- Reusable client factories ----- #


def get_mgmt_client():
    """Return an Auth0 Management API client."""
    return UserManagement(AUTH0_DOMAIN, AUTH0_CLIENT_ID)


def get_auth_client():
    """Return an Auth0 Authentication API client for user login flows."""
    return Users(AUTH0_DOMAIN, AUTH0_CLIENT_ID)


def get_tokens_client():
    """Return an Auth0 Tokens client for token exchange."""
    return Tokens(AUTH0_DOMAIN, AUTH0_CLIENT_ID)


# ----- Example helper wrappers (optional) ----- #
def create_user(email, password, connection="Username-Password-Authentication"):
    mgmt = get_mgmt_client()
    user = {
        "email": email,
        "password": password,
        "connection": connection,
        "email_verified": False,
    }
    return mgmt.create_user(user)


# End of helper module
