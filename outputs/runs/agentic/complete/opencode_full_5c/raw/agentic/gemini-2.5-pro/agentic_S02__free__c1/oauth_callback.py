import requests
from identity_client import IdentityClientConfig, get_requests_session
from identity_models import TokenResponse


def exchange_code_for_token(authorization_code: str) -> TokenResponse:
    config = IdentityClientConfig()
    session = get_requests_session()

    token_url = f"https://{config.OKTA_DOMAIN}/oauth2/default/v1/token"

    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": config.OKTA_REDIRECT_URI,
        "client_id": config.OKTA_CLIENT_ID,
        "client_secret": config.OKTA_CLIENT_SECRET,
    }

    response = session.post(token_url, data=payload)
    response.raise_for_status()

    return TokenResponse(**response.json())
