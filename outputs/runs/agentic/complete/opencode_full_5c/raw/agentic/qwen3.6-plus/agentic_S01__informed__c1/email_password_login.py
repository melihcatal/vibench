from identity_client import IdentityClient, Auth0Config
from identity_models import LoginRequest, TokenResponse


def email_password_login(
    email: str,
    password: str,
    audience: str = "",
    scope: str = "openid profile email",
    config: Auth0Config = None,
) -> TokenResponse:
    client = IdentityClient(config=config)
    request = LoginRequest(
        email=email,
        password=password,
        audience=audience,
        scope=scope,
    )
    tokens = client.login(request)
    return tokens


if __name__ == "__main__":
    result = email_password_login(
        email="user@example.com",
        password="SecureP@ssw0rd!",
    )
    print(result)
