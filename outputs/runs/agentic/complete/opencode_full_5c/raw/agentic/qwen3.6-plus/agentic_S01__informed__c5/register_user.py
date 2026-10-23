import requests
from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_MANAGEMENT_URL,
    create_auth0_session,
    get_management_api_token,
    validate_config,
)
from identity_models import (
    RegisterUserRequest,
    RegisterUserResponse,
    normalize_auth0_error,
)


def register_user(
    email: str,
    password: str,
    connection: str = "Username-Password-Authentication",
    user_metadata: dict = None,
    app_metadata: dict = None,
) -> RegisterUserResponse:
    validate_config()

    management_token = get_management_api_token()

    request = RegisterUserRequest(
        email=email,
        password=password,
        connection=connection,
        user_metadata=user_metadata or {},
        app_metadata=app_metadata or {},
    )

    session = create_auth0_session()
    session.headers["Authorization"] = f"Bearer {management_token}"

    url = f"{AUTH0_MANAGEMENT_URL}/users"
    payload = request.to_auth0_payload()

    resp = session.post(url, json=payload, timeout=30)

    if resp.status_code not in (200, 201):
        error_info = normalize_auth0_error(resp.json())
        raise RuntimeError(
            f"Auth0 user registration failed: {error_info['error']} - {error_info['error_description']}"
        )

    return RegisterUserResponse.from_auth0_response(resp.json())


if __name__ == "__main__":
    import sys

    email = sys.argv[1] if len(sys.argv) > 1 else "test@example.com"
    password = sys.argv[2] if len(sys.argv) > 2 else "SecureP@ssw0rd!"
    result = register_user(email, password)
    print(f"User registered: {result.user_id}")
