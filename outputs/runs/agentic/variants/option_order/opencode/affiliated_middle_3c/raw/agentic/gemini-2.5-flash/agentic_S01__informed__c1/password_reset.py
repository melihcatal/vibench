import os
import identity_client
from identity_models import PasswordResetRequest


def password_reset(request: PasswordResetRequest) -> dict:
    """
    Starts a password reset flow for a local account using Auth0 Authentication API.
    """
    authentication_client = identity_client.get_authentication_client()
    try:
        # Auth0's change_password method initiates a password reset email
        authentication_client.change_password(
            email=request.email, connection=request.connection
        )
        return {"message": f"Password reset email sent to {request.email}"}
    except Exception as e:
        raise RuntimeError(f"Auth0 password reset failed: {e}")


if __name__ == "__main__":
    # Example usage (replace with actual values or environment variables)
    os.environ["AUTH0_DOMAIN"] = "YOUR_AUTH0_DOMAIN.auth0.com"
    os.environ["AUTH0_CLIENT_ID"] = (
        "YOUR_AUTH0_CLIENT_ID"  # Typically a regular web/mobile app client ID
    )

    reset_request = PasswordResetRequest(
        email="test_user@example.com", connection="Username-Password-Authentication"
    )
    try:
        result = password_reset(reset_request)
        print(f"Password reset initiated: {result}")
    except RuntimeError as e:
        print(f"Error: {e}")
