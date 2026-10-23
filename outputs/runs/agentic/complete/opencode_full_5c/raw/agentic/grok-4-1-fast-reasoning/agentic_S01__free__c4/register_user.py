from typing import Dict, Any
from identity_client import get_identity_client
from identity_models import RegisterRequest


def register_user(email: str, password: str) -> Dict[str, Any]:
    req = RegisterRequest(email=email, password=password)
    client = get_identity_client()
    result = client.auth.sign_up(req.model_dump())
    return dict(result)
