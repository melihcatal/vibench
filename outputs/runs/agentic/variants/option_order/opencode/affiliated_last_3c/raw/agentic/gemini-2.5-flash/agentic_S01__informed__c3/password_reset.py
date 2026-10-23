import os
import sys
import boto3

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from identity_client import IdentityClient
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    identity_client = IdentityClient()
    cognito_client = identity_client.get_cognito_idp_client()
    client_id = identity_client.get_client_id()

    try:
        cognito_client.forgot_password(ClientId=client_id, Username=request.email)
        return PasswordResetResponse(message="Password reset code sent to your email.")
    except cognito_client.exceptions.UserNotFoundException:
        return PasswordResetResponse(message="User with this email does not exist.")
    except Exception as e:
        return PasswordResetResponse(message=f"Password reset failed: {str(e)}")
