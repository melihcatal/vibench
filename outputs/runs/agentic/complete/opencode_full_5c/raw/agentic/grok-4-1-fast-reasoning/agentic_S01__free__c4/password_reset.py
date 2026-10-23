from identity_client import get_identity_client
from identity_models import ResetRequest
from typing import Dict, Any


def password_reset(email: str) -> Dict[str, Any]:
    client = get_identity_client()
    result = client.auth.reset_password_for_email(email)
    return dict(result)
