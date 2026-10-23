import os
import requests
from identity_client import IdentityClient
from identity_models import RegisterRequest, RegisterResponse

# AuthService API (third‑party SaaS) configuration loaded from env vars
BASE_URL = os.getenv("AUTH_SERVICE_BASE_URL", "https://api.authservice.example.com")
API_KEY = os.getenv("AUTH_SERVICE_API_KEY")


def register_user(email: str, password: str, **kwargs) -> RegisterResponse:
    """Create a new email/password user account using AuthService SaaS.
    Returns RegisterResponse with user ID and token data.
    """
    payload = RegisterRequest(
        email=email,
        password=password,
        locale=kwargs.get("locale"),
        metadata=kwargs.get("metadata"),
    ).to_dict()

    client = IdentityClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/register", json=payload)
    return RegisterResponse.from_dict(response.json())
