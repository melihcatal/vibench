import os
from identity_client import load_identity_config, create_auth0_client, IdentityConfig
from identity_models import RefreshRequest, RefreshResponse


def refresh_session(
    refresh_token: str,
    audience: str = "",
    config: IdentityConfig = None,
) -> RefreshResponse:
    config = config or load_identity_config()
    client = create_auth0_client(config)

    refresh = RefreshRequest(
        refresh_token=refresh_token,
        audience=audience or config.audience,
    )

    payload = refresh.to_auth0_payload(client_id=config.client_id)

    oauth_url = client.config.get_oauth_token_url()
    resp = client.post(oauth_url, payload)
    resp.raise_for_status()
    data = resp.json()

    client.close()
    return RefreshResponse.from_auth0_response(data)


if __name__ == "__main__":
    result = refresh_session(
        refresh_token=os.environ.get("TEST_REFRESH_TOKEN", ""),
    )
    print(result)
