from identity_client import CognitoIdentityClient
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(email: str) -> dict:
    client = CognitoIdentityClient()
    request = PasswordResetRequest(email=email)
    response = client.start_password_reset(email=request.email)
    return PasswordResetResponse(**response).dict()
