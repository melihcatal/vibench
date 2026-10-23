import identity_client


def start_password_reset(email):
    """Initiate a password reset flow for a local Auth0 user account.
    Sends a password reset email and returns the reset ticket or raises an exception.
    """
    payload = {
        "client_id": identity_client.AUTH0_CLIENT_ID,
        "email": email,
        "connection": "Username-Password-Authentication",
    }
    identity_client.auth0_client.initiate_password_reset(payload)
