from identity_client import IdentityClient
from identity_models import PasswordResetRequest

def password_reset(email: str):
    client = IdentityClient()
    request = PasswordResetRequest(email=email)
    response = client.send_password_reset_email(request)
    return response
