import os
from identity_client import IdentityClient
from identity_models import ForgotPasswordRequest, ForgotPasswordSubmitRequest, PasswordResetResponse

# Using AWS Cognito User Pools as the concrete external provider
# Environment variables expected: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, COGNITO_USER_POOL_ID, COGNITO_CLIENT_ID

client = IdentityClient(
    service='cognito',
    region=os.getenv('AWS_REGION'),
    user_pool=os.getenv('COGNITO_USER_POOL_ID'),
    client_id=os.getenv('COGNITO_CLIENT_ID')
)

def start_password_reset(email: str):
    """Initiates a password reset flow for a local account via Cognito.
    Returns the code delivery details, to be used with submit_password_reset.
    """    request = ForgotPasswordRequest(username=email)
    response = client.forgot_password(request)
    return response

def submit_password_reset(email: str, confirmation_code: str, new_password: str):
    """Completes the password reset after providing the verification code.
    Returns PasswordResetResponse indicating success.
    """    request = ForgotPasswordSubmitRequest(
        username=email,
        confirmation_code=confirmation_code,
        password=new_password
    )
    response = client.confirm_forgot_password(request)
    return PasswordResetResponse(**response)
