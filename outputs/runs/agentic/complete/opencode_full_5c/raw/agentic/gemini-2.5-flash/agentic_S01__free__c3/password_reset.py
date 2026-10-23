import os
import boto3
from identity_models import PasswordResetRequest, PasswordResetResponse
from identity_client import (
    get_cognito_client,
    get_cognito_user_pool_id,
    get_cognito_client_id,
)


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    cognito_client = get_cognito_client()
    client_id = request.client_id

    try:
        # Note: Cognito's forgot_password does not require client_id in the API call itself
        # but it's good practice to include it in the request object for consistency
        response = cognito_client.forgot_password(
            ClientId=client_id,  # Cognito API expects ClientId here for some reason.
            Username=request.email,
        )
        # Cognito's forgot_password response doesn't contain much detail,
        # primarily status code. A successful call means an email/SMS was sent.
        return PasswordResetResponse(
            message="Password reset initiated. Check your email/phone for instructions."
        )
    except cognito_client.exceptions.UserNotFoundException:
        # It's generally safer not to expose if a user exists for security reasons
        # but for this example, we'll explicitly state it. In production,
        # you might return a generic success message to prevent user enumeration.
        raise ValueError(
            "If a user with this email exists, a password reset email has been sent."
        )
    except Exception as e:
        raise RuntimeError(f"Cognito password reset failed: {e}")


if __name__ == "__main__":
    # Example usage (requires environment variables to be set)
    os.environ["AWS_REGION"] = "us-east-1"
    os.environ["COGNITO_USER_POOL_ID"] = (
        "YOUR_USER_POOL_ID"  # Not directly used by forgot_password but for client setup
    )
    os.environ["COGNITO_CLIENT_ID"] = "YOUR_CLIENT_ID"

    try:
        reset_request = PasswordResetRequest(
            email="testuser@example.com",
            client_id=get_cognito_client_id(),
            user_pool_id=get_cognito_user_pool_id(),
        )
        response = password_reset(reset_request)
        print(f"Password reset status: {response.message}")
    except Exception as e:
        print(f"Error during password reset: {e}")
