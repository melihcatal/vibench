import os
from identity_client import load_identity_config, create_auth0_client, IdentityConfig
from identity_models import LoginRequest, LoginResponse


def email_password_login(
    email: str,
    password: str,
    audience: str = "",
    scope: str = "openid profile email",
    config: IdentityConfig = None,
) -> LoginResponse:
    config = config or load_identity_config()
    client = create_auth0_client(config)

    login = LoginRequest(
        email=email,
        password=password,
        audience=audience or config.audience,
        scope=scope,
    )

    payload = login.to_auth0_payload(client_id=config.client_id)

    oauth_url = client.config.get_oauth_token_url()
    resp = client.post(oauth_url, payload)
    resp.raise_for_status()
    data = resp.json()

    client.close()
    return LoginResponse.from_auth0_response(data)


if __name__ == "__main__":
    result = email_password_login(
        email=os.environ.get("TEST_EMAIL", "user@example.com"),
        password=os.environ.get("TEST_PASSWORD", "SecureP@ssw0rd!"),
    )
    print(result)
