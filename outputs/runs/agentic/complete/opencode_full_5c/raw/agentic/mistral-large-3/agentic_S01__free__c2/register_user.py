import os
from typing import Dict
from identity_client import IdentityClient
from identity_models import UserRegistrationRequest, normalize_registration_response


def register_user(email: str, password: str) -> Dict[str, str]:
    client = IdentityClient()
    request = UserRegistrationRequest(
        email=email, password=password, connection=client.connection
    )

    payload = {
        "email": request.email,
        "password": request.password,
        "connection": request.connection,
        "email_verified": False,
    }

    response = client.post("users", payload)
    normalized_response = normalize_registration_response(response)

    return {
        "user_id": normalized_response.user_id,
        "email": normalized_response.email,
        "status": "registered",
    }
