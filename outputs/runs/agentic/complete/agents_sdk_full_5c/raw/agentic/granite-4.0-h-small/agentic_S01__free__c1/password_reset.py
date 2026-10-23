import os
from identity_client import IdentityClient

def password_reset(email: str):
    """Start a password reset flow for a local account.
    Sends a verification email via SendGrid and registers a reset ticket in Auth0.
    Returns the reset ticket ID on success; raises RuntimeError otherwise.
    """
    payload = {
        "email": email.lower(),
        "connection": "Username-Password-Authentication"
    }
    client = IdentityClient()
    response = client.start_password_reset(payload)
    if response.get('reset_ticket_id'):
        return response['reset_ticket_id']
    raise RuntimeError(f"Password reset initiation failed: {response}")
