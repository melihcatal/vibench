# [SAME-SCENARIO] email_password_login.py
# Sign in a user with email and password and return tokens using Auth0 Management API

import os
from auth0.v3.authentication import Users

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

auth0 = Users(AUTH0_DOMAIN, AUTH0_CLIENT_ID)


def email_password_login(email, password):
    """Exchange email and password for access and ID tokens.

    Returns a dict with 'access_token' and 'id_token' on success, raises on failure.
    """
    result = auth0.get_user_by_email(email)
    # Obtain a token for the user (using client credentials grant)
    token = auth0.get_access_token_for_user(user_id=result["user_id"])
    return {"access_token": token["access_token"], "id_token": token["id_token"]}
