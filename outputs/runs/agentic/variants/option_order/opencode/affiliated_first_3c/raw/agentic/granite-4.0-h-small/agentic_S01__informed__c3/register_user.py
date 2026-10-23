import identity_client


def register_user(email, password):
    """Create a new email/password user account using Auth0.
    Returns user metadata on success or raises an exception.
    """
    payload = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
    }
    identity_client.auth0_client.create_user(payload)
