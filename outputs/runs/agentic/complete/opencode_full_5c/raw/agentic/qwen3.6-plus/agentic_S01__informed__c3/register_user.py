import os
import requests
from identity_client import load_identity_config, create_auth0_client, IdentityConfig
from identity_models import UserRegistrationRequest, UserRegistrationResponse


AUTH0_MANAGEMENT_API_URL = "https://{domain}/api/v2/users"


def register_user(
    email: str,
    password: str,
    given_name: str = "",
    family_name: str = "",
    metadata: dict = None,
    config: IdentityConfig = None,
) -> UserRegistrationResponse:
    config = config or load_identity_config()
    client = create_auth0_client(config)

    registration = UserRegistrationRequest(
        email=email,
        password=password,
        given_name=given_name,
        family_name=family_name,
        metadata=metadata or {},
    )

    payload = registration.to_auth0_payload()

    management_url = AUTH0_MANAGEMENT_API_URL.format(domain=config.domain)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.management_token}",
    }

    resp = client.post(management_url, payload, headers=headers)
    resp.raise_for_status()
    data = resp.json()

    client.close()
    return UserRegistrationResponse.from_auth0_response(data)


if __name__ == "__main__":
    result = register_user(
        email=os.environ.get("TEST_EMAIL", "newuser@example.com"),
        password=os.environ.get("TEST_PASSWORD", "SecureP@ssw0rd!"),
        given_name="New",
        family_name="User",
    )
    print(result)
