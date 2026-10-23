import os
import requests
from identity_client import IdentityClient
from identity_models import LoginRequest, LoginResponse

# AuthService API (third‑party SaaS) configuration loaded from env vars
BASE_URL = os.getenv("AUTH_SERVICE_BASE_URL", "https://api.authservice.example.com")
API_KEY = os.getenv("AUTH_SERVICE_API_KEY")


def email_password_login(email: str, password: str, **kwargs) -> LoginResponse:
    """Sign in a user with email and password and return authentication tokens.
    Returns LoginResponse containing access and refresh tokens.
    """
    payload = LoginRequest(
        email=email,
        password=password,
        device_info=kwargs.get("device_info"),
    ).to_dict()

    client = IdentityClient(base_url=BASE_URL, api_key=API_KEY)
    response = client.post("/v1/login", json=payload)
    return LoginResponse.from_dict(response.json())
