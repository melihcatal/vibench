import os
from typing import Dict
from identity_client import IdentityClient
from identity_models import PasswordResetRequest


def password_reset(email: str) -> Dict[str, str]:
    client = IdentityClient()
    request = PasswordResetRequest(email=email, connection=client.connection)

    payload = {
        "email": request.email,
        "connection": request.connection,
        "client_id": os.getenv("AUTH0_CLIENT_ID"),
    }

    response = client.post("dbconnections/change_password", payload)

    return {
        "status": "reset_email_sent",
        "message": f"Password reset email sent to {email}",
    }
