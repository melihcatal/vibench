import requests
from identity_client import (
    AUTH0_CLIENT_ID,
    AUTH0_AUDIENCE,
    AUTH0_AUTH_URL,
    create_auth0_session,
    validate_config,
)
from identity_models import (
    RefreshSessionRequest,
    RefreshSessionResponse,
    normalize_auth0_error,
)


def refresh_session(
    refresh_token: str, audience: str = None, scope: str = None
) -> RefreshSessionResponse:
    validate_config()

    request = RefreshSessionRequest(
        refresh_token=refresh_token,
        audience=audience or AUTH0_AUDIENCE,
        scope=scope,
    )

    session = create_auth0_session()
    payload = request.to_auth0_payload(AUTH0_CLIENT_ID)

    resp = session.post(AUTH0_AUTH_URL, json=payload, timeout=30)

    if resp.status_code != 200:
        error_info = normalize_auth0_error(resp.json())
        raise RuntimeError(
            f"Auth0 token refresh failed: {error_info['error']} - {error_info['error_description']}"
        )

    return RefreshSessionResponse.from_auth0_response(resp.json())


if __name__ == "__main__":
    import sys

    token = sys.argv[1] if len(sys.argv) > 1 else ""
    result = refresh_session(token)
    print(f"Session refreshed. New access token: {result.access_token[:20]}...")
