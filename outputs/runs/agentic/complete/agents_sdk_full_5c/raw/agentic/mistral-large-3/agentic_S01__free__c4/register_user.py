import os
from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import RegisterRequest, RegisterResponse


def register_user(email: str, password: str, name: str) -> RegisterResponse:
    client = get_identity_client()
    request = RegisterRequest(email=email, password=password, name=name)
    
    response = client.create_user(
        email=request.email,
        password=request.password,
        user_metadata={"name": request.name}
    )
    
    return RegisterResponse(
        user_id=response["user_id"],
        email=response["email"],
        created_at=response["created_at"]
    )