import identity_client


def email_password_login(email, password):
    """Sign in a user with email and password using Auth0 and return ID/Access tokens.
    Raises an exception on authentication failure.
    """
    payload = {
        "email": email,
        "password": password,
        "client_id": identity_client.AUTH0_CLIENT_ID,
        "client_secret": identity_client.AUTH0_CLIENT_SECRET,
        "audience": identity_client.AUTH0_AUDIENCE,
        "grant_type": "password",
    }
    return identity_client.auth0_client.exchange_password_for_tokens(payload)
