from identity_client import IdentityClient
from identity_models import PasswordResetRequest, PasswordResetResponse

def password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    identity_client = IdentityClient()
    result = identity_client.initiate_password_reset(request.email)
    if "message" in result:
        return PasswordResetResponse(message=result["message"])
    else:
        raise Exception(result.get("error", "Unknown password reset error"))
