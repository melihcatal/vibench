from identity_models import PasswordResetRequest, PasswordResetResponse
from identity_client import IdentityClient

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    identity_client = IdentityClient()
    reset_result = identity_client.password_reset(request.email)

    return PasswordResetResponse(
        message=reset_result["message"]
    )
