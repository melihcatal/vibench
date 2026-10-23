from identity_client import get_firebase_client
from identity_models import PasswordResetRequest, PasswordResetResponse


def initiate_password_reset(request: PasswordResetRequest) -> PasswordResetResponse:
    auth = get_firebase_client()
    try:
        response = auth.send_password_reset_email(request.email)
        # The pyrebase library returns a simple dict on success
        # which we can model if we want more structure.
        # For now, we'll assume it looks like this on success
        return PasswordResetResponse(email=request.email, kind="sendOobCode")
    except Exception as e:
        raise e
