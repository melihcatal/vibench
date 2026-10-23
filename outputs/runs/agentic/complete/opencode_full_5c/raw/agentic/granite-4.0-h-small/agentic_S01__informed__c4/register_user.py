from identity_client import IdentityClient

# SAME-SCENARIO: Register a new email/password user account


def register_user(email: str, password: str, client: IdentityClient):
    """Create a new local email/password account.

    Args:
        email: User's email address.
        password: Password for the new account.
        client: IdentityClient configured with the target provider.

    Returns:
        dict: Provider-specific user object / confirmation response.
    """
    payload = client.build_register_payload(email=email, password=password)
    response = client.call_api("POST", "/register", json=payload)
    client.validate_response(response, "register")
    return response.json()
