import requests
from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_DB_CONNECTIONS_URL,
    create_auth0_session,
    validate_config,
)
from identity_models import (
    PasswordResetRequest,
    PasswordResetResponse,
    normalize_auth0_error,
)


def password_reset(
    email: str, connection: str = "Username-Password-Authentication"
) -> PasswordResetResponse:
    validate_config()

    request = PasswordResetRequest(
        email=email,
        connection=connection,
    )

    session = create_auth0_session()
    payload = request.to_auth0_payload(AUTH0_CLIENT_ID)

    url = f"{AUTH0_DB_CONNECTIONS_URL}/change_password"
    resp = session.post(url, json=payload, timeout=30)

    if resp.status_code not in (200, 201):
        error_info = normalize_auth0_error(resp.json())
        raise RuntimeError(
            f"Auth0 password reset failed: {error_info['error']} - {error_info['error_description']}"
        )

    return PasswordResetResponse.from_auth0_response(
        resp.json(), email=email, connection=connection
    )


if __name__ == "__main__":
    import sys

    email = sys.argv[1] if len(sys.argv) > 1 else "user@example.com"
    result = password_reset(email)
    print(f"Password reset initiated for: {result.email}")
