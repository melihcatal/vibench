from identity_client import IdentityClient, Auth0Config
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(
    email: str,
    connection: str = "Username-Password-Authentication",
    client_id: str = "",
    config: Auth0Config = None,
) -> PasswordResetResponse:
    client = IdentityClient(config=config)
    request = PasswordResetRequest(
        email=email,
        connection=connection,
        client_id=client_id,
    )
    result = client.initiate_password_reset(request)
    return result


if __name__ == "__main__":
    result = password_reset(
        email="user@example.com",
    )
    print(result)
