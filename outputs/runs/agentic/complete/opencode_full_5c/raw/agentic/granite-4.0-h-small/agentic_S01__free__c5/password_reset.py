import os
import requests
from identity_client import IdentityClient
from identity_models import ResetRequest, ResetResponse

# AuthService API (third‑party SaaS) configuration loaded from env vars
BASE_URL = os.getenv("AUTH_SERVICE_BASE_URL", "https://api.authservice.example.com")
API_KEY = os.getenv("AUTH_SERVICE_API_KEY")


def password_reset(email: str, **kwargs) -> ResetResponse:
    """Initiate a password reset flow for a local account.
    Returns ResetResponse containing reset token or instructions URL.
    """
    payload = ResetRequest(email=email, **kwargs).to_dict()

    client = IdentityClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/reset-password", json=payload)
    return ResetResponse.from_dict(response.json())
