import os
import httpx
from identity_models import RegisterRequest, RegisterResponse, normalize_email
from identity_client import (
    Auth0ClientConfig,
    AUTH0_USER_REGISTRATION_URL,
    parse_auth0_error,
)


def register_user(
    email: str,
    password: str,
    client_id: str = None,
    user_metadata: dict = None,
    app_metadata: dict = None,
    connection: str = "Username-Password-Authentication",
) -> RegisterResponse:
    config = Auth0ClientConfig()
    normalized_email = normalize_email(email)

    request = RegisterRequest(
        email=normalized_email,
        password=password,
        connection=connection,
        client_id=client_id or config.client_id,
        user_metadata=user_metadata or {},
        app_metadata=app_metadata or {},
    )

    payload = request.to_payload()

    headers = config.get_management_headers()

    with httpx.Client(timeout=30) as client:
        response = client.post(
            AUTH0_USER_REGISTRATION_URL,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()

    return RegisterResponse.from_auth0_response(data)


if __name__ == "__main__":
    email = os.environ.get("TEST_USER_EMAIL", "newuser@example.com")
    password = os.environ.get("TEST_USER_PASSWORD", "SecurePass123!")
    result = register_user(email=email, password=password)
    print(f"Registered user: {result.user_id} ({result.email})")
