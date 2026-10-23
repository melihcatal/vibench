import os
from identity_client import load_identity_config, create_auth0_client, IdentityConfig
from identity_models import PasswordResetRequest, PasswordResetResponse


def password_reset(
    email: str,
    connection: str = "Username-Password-Authentication",
    config: IdentityConfig = None,
) -> PasswordResetResponse:
    config = config or load_identity_config()
    client = create_auth0_client(config)

    reset = PasswordResetRequest(
        email=email,
        connection=connection,
    )

    payload = reset.to_auth0_payload(client_id=config.client_id)

    change_password_url = client.config.get_db_connection_change_password_url()
    resp = client.post(change_password_url, payload)
    resp.raise_for_status()
    data = resp.json()

    client.close()
    return PasswordResetResponse.from_auth0_response(data)


if __name__ == "__main__":
    result = password_reset(
        email=os.environ.get("TEST_EMAIL", "user@example.com"),
    )
    print(result)
