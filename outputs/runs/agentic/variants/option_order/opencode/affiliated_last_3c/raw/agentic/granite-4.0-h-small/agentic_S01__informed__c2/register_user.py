# [SAME-SCENARIO] register_user.py
# Creates a new email/password user account using Auth0 Management API

import os
from auth0.v3.management import UserManagement

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

# Initialize the Auth0 client
auth0 = UserManagement(AUTH0_DOMAIN, AUTH0_CLIENT_ID)


def register_user(email, password, connection="Username-Password-Authentication"):
    """Create a new user with email and password.

    Returns the created user ID on success, raises an exception on failure.
    """
    user = {
        "email": email,
        "password": password,
        "connection": connection,
        "email_verified": False,
    }
    return auth0.create_user(user)
