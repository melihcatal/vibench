from identity_client import IdentityClient

# SAME-SCENARIO: Initiate password reset for a local account


def password_reset(email: str, client: IdentityClient):
    """Start a password reset flow for a user with a local email/password account.

    Args:
        email: The email address whose password will be reset.
        client: IdentityClient configured with the target provider.

    Returns:
        dict: Confirmation payload from the provider (contains reset token/link if applicable).
    """
    payload = client.build_reset_payload(email=email)
    response = client.call_api("POST", "/password/reset", json=payload)
    client.validate_response(response, "password_reset")
    return response.json()
