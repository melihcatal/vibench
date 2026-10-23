import os
from auth0.authentication import Auth0Authentication
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    domain = os.environ.get("AUTH0_DOMAIN")
    client_id = os.environ.get("AUTH0_CLIENT_ID")

    auth0 = Auth0Authentication(domain, client_id)

    response = auth0.change_password(
        request.email,
        os.environ.get("AUTH0_DB_CONNECTION", "Username-Password-Authentication"),
    )

    # Auth0's change_password method typically returns a success message or None on success.
    # We'll adapt the response model to reflect this.
    message = (
        response.get("message", "Password reset email sent.")
        if isinstance(response, dict)
        else "Password reset email sent."
    )
    return PasswordResetResponse(message=message)
