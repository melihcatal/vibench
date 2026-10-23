import os
from identity_client import IdentityClient
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> Dict[str, Any]:
    identity_client = IdentityClient()
    # Auth0's change_password method is used to initiate a password reset flow.
    # It typically sends an email to the user with a link to reset their password.
    response = identity_client.authentication_client.change_password(
        client_id=request.client_id,
        email=request.email,
        connection=request.connection,
    )
    # The response for change_password is typically a success message or None if successful.
    # We'll return a dictionary indicating success for consistency.
    return {
        "message": f"Password reset email sent to {request.email}",
        "response": response,
    }
