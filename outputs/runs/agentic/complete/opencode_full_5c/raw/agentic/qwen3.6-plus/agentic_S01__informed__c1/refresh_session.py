from identity_client import IdentityClient, Auth0Config
from identity_models import RefreshTokenRequest, TokenResponse


def refresh_session(
    refresh_token: str,
    audience: str = "",
    scope: str = "openid profile email",
    config: Auth0Config = None,
) -> TokenResponse:
    client = IdentityClient(config=config)
    request = RefreshTokenRequest(
        refresh_token=refresh_token,
        audience=audience,
        scope=scope,
    )
    tokens = client.refresh_session(request)
    return tokens


if __name__ == "__main__":
    result = refresh_session(
        refresh_token="eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
    )
    print(result)
