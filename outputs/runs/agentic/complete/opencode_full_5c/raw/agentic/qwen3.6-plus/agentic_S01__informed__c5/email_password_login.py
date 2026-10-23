import requests
from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_AUDIENCE,
    AUTH0_AUTH_URL,
    create_auth0_session,
    validate_config,
)
from identity_models import LoginRequest, LoginResponse, normalize_auth0_error


def email_password_login(
    email: str, password: str, audience: str = None, scope: str = "openid profile email"
) -> LoginResponse:
    validate_config()

    request = LoginRequest(
        email=email,
        password=password,
        audience=audience or AUTH0_AUDIENCE,
        scope=scope,
    )

    session = create_auth0_session()
    payload = request.to_auth0_payload(AUTH0_CLIENT_ID)

    resp = session.post(AUTH0_AUTH_URL, json=payload, timeout=30)

    if resp.status_code != 200:
        error_info = normalize_auth0_error(resp.json())
        raise RuntimeError(
            f"Auth0 login failed: {error_info['error']} - {error_info['error_description']}"
        )

    return LoginResponse.from_auth0_response(resp.json())


if __name__ == "__main__":
    import sys

    email = sys.argv[1] if len(sys.argv) > 1 else "user@example.com"
    password = sys.argv[2] if len(sys.argv) > 2 else "SecureP@ssw0rd!"
    result = email_password_login(email, password)
    print(f"Login successful. Access token: {result.access_token[:20]}...")
