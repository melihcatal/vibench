import requests

from identity_client import auth0_domain, auth0_token_payload, request_timeout
from identity_models import LoginRequest, normalize_auth0_token_response


def email_password_login(request: LoginRequest):
    response = requests.post(
        f"https://{auth0_domain()}/oauth/token",
        json=auth0_token_payload(
            username=request.email,
            password=request.password,
            scope=request.scope,
            audience=request.audience,
        ),
        timeout=request_timeout(),
    )
    response.raise_for_status()
    return normalize_auth0_token_response(response.json())
