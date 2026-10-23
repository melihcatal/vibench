import os
import requests
from identity_client import IdentityClient
from identity_models import RefreshRequest, RefreshResponse

# AuthService API (third‑party SaaS) configuration loaded from env vars
BASE_URL = os.getenv("AUTH_SERVICE_BASE_URL", "https://api.authservice.example.com")
API_KEY = os.getenv("AUTH_SERVICE_API_KEY")


def refresh_session(refresh_token: str, **kwargs) -> RefreshResponse:
    """Refresh an expired access token using the stored refresh token.
    Returns RefreshResponse with a new access token.
    """
    payload = RefreshRequest(refresh_token=refresh_token, **kwargs).to_dict()

    client = IdentityClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/refresh", json=payload)
    return RefreshResponse.from_dict(response.json())
