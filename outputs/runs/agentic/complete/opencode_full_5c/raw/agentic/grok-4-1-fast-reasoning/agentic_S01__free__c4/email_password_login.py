from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import LoginRequest


def email_password_login(email: str, password: str) -> Dict[str, Any]:
    req = LoginRequest(email=email, password=password)
    client = get_identity_client()
    result = client.auth.sign_in_with_password(req.model_dump())
    return dict(result)
