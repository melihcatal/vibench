from identity_client import AWSClient
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    aws_client = AWSClient()
    cognito_client = aws_client.get_cognito_client()
    client_id = aws_client.get_client_id()

    try:
        cognito_client.forgot_password(
            ClientId=client_id,
            Username=request.email
        )
        return PasswordResetResponse(message="Password reset initiated. Check your email for a verification code.")
    except cognito_client.exceptions.UserNotFoundException:
        return PasswordResetResponse(message="User not found.")
    except Exception as e:
        return PasswordResetResponse(message=f"Password reset failed: {str(e)}")
