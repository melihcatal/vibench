import os
from identity_client import IdentityClient
from identity_models import PasswordResetRequest

def password_reset(email):
    client = IdentityClient(api_key=os.environ.get("FIREBASE_API_KEY"))
    reset_request = PasswordResetRequest(email=email)
    response = client.send_password_reset_email(reset_request)
    return {"status": "Password reset email sent to", "email": response["email"]}
