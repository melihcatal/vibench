import os
import httpx
from identity_models import RefreshRequest, RefreshResponse
from identity_client import (
    Auth0ClientConfig,
    AUTH0_OAUTH_TOKEN_URL,
    parse_auth0_error,
)


def refresh_session(
    refresh_token: str,
    client_id: str = None,
) -> RefreshResponse:
    config = Auth0ClientConfig()

    request = RefreshRequest(
        refresh_token=refresh_token,
        client_id=client_id or config.client_id,
    )

    payload = request.to_payload(client_id=config.client_id)

    headers = config.get_oauth_headers()

    with httpx.Client(timeout=30) as client:
        response = client.post(
            AUTH0_OAUTH_TOKEN_URL,
            json=payload,
            headers=headers,
        )
        response.raise_for_status()
        data = response.json()

    return RefreshResponse.from_auth0_response(data)


if __name__ == "__main__":
    refresh_token = os.environ.get("TEST_REFRESH_TOKEN", "")
    result = refresh_session(refresh_token=refresh_token)
    print(f"Session refreshed. New access token: {result.access_token[:20]}...")
    print(f"New expires in: {result.expires_in}s")
