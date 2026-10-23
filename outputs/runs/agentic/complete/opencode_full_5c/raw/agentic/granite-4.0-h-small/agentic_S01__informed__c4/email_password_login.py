from identity_client import IdentityClient

# SAME-SCENARIO: SignIn with email and password and return tokens


def email_password_login(email: str, password: str, client: IdentityClient):
    """Authenticate a user via email/password and retrieve tokens.

    Args:
        email: User's email address.
        password: Password for the account.
        client: IdentityClient configured with the target provider.

    Returns:
        dict: Provider-specific token response.
    """
    payload = client.build_login_payload(email=email, password=password)
    response = client.call_api("POST", "/token", json=payload)
    client.validate_response(response, "login")
    return response.json()
