from identity_client import IdentityClient, Auth0Config
from identity_models import RegisterUserRequest, UserResponse


def register_user(
    email: str,
    password: str,
    given_name: str = "",
    family_name: str = "",
    locale: str = "en",
    metadata: dict = None,
    config: Auth0Config = None,
) -> UserResponse:
    client = IdentityClient(config=config)
    request = RegisterUserRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
        locale=locale,
        metadata=metadata or {},
    )
    user = client.register_user(request)
    return user


if __name__ == "__main__":
    result = register_user(
        email="newuser@example.com",
        password="SecureP@ssw0rd!",
        given_name="Jane",
        family_name="Doe",
        locale="en",
    )
    print(result)
