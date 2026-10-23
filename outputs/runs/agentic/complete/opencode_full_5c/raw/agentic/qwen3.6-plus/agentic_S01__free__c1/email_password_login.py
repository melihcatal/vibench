import os
import httpx
from identity_models import LoginRequest, LoginResponse, normalize_email
from identity_client import (
    Auth0ClientConfig,
    AUTH0_OAUTH_TOKEN_URL,
    parse_auth0_error,
)


def email_password_login(
    email: str,
    password: str,
    client_id: str = None,
    audience: str = None,
    scope: str = "openid profile email",
) -> LoginResponse:
    config = Auth0ClientConfig()
    normalized_email = normalize_email(email)

    request = LoginRequest(
        email=normalized_email,
        password=password,
        client_id=client_id or config.client_id,
        audience=audience or config.audience,
        scope=scope,
    )

    payload = request.to_payload(client_id=config.client_id)

    headers = config.get_oauth_headers()

    with httpx.Client(timeout=30) as client:
        response = client.post(
            AUTH0_OAUTH_TOKEN_URL,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()

    return LoginResponse.from_auth0_response(data)


if __name__ == "__main__":
    email = os.environ.get("TEST_USER_EMAIL", "user@example.com")
    password = os.environ.get("TEST_USER_PASSWORD", "SecurePass123!")
    result = email_password_login(email=email, password=password)
    print(f"Login successful. Access token: {result.access_token[:20]}...")
    print(f"ID token: {result.id_token[:20]}...")
    print(f"Expires in: {result.expires_in}s")
