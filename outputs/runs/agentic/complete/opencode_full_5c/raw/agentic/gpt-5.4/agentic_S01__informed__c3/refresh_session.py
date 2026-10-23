import requests

from identity_client import auth0_domain, auth0_token_payload, request_timeout
from identity_models import RefreshSessionRequest, normalize_auth0_token_response


def refresh_session(request: RefreshSessionRequest):
    response = requests.post(
        f"https://{auth0_domain()}/oauth/token",
        json=auth0_token_payload(
            username="", refresh_token=request.refresh_token, scope=request.scope
        ),
        timeout=request_timeout(),
    )
    response.raise_for_status()
    return normalize_auth0_token_response(response.json())
