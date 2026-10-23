import os
import httpx
from identity_models import PasswordResetRequest, PasswordResetResponse, normalize_email
from identity_client import (
    Auth0ClientConfig,
    AUTH0_PASSWORD_CHANGE_URL,
    parse_auth0_error,
)


def password_reset(
    email: str,
    client_id: str = None,
    connection: str = "Username-Password-Authentication",
) -> PasswordResetResponse:
    config = Auth0ClientConfig()
    normalized_email = normalize_email(email)

    request = PasswordResetRequest(
        email=normalized_email,
        connection=connection,
        client_id=client_id or config.client_id,
    )

    payload = request.to_payload(client_id=config.client_id)

    headers = config.get_oauth_headers()

    with httpx.Client(timeout=30) as client:
        response = client.post(
            AUTH0_PASSWORD_CHANGE_URL,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()

    return PasswordResetResponse.from_auth0_response(data)


if __name__ == "__main__":
    email = os.environ.get("TEST_USER_EMAIL", "user@example.com")
    result = password_reset(email=email)
    print(f"Password reset initiated for: {result.email}")
    print(f"Message: {result.message}")
