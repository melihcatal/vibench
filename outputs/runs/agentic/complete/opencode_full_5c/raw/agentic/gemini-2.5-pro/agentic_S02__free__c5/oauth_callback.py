import os
import requests
from identity_client import get_okta_oauth_config
from identity_models import OAuthState


def exchange_code_for_tokens(authorization_code: str, oauth_state: OAuthState):
    """
    Exchanges an authorization code for access and ID tokens from Okta.
    """
    okta_config = get_okta_oauth_config()

    token_url = f"{okta_config['issuer']}/v1/token"

    payload = {
        "grant_type": "authorization_code",
        "code": authorization_code,
        "redirect_uri": okta_config["redirect_uri"],
    }

    response = requests.post(
        token_url,
        auth=(okta_config["client_id"], okta_config["client_secret"]),
        data=payload,
    )

    response.raise_for_status()
    return response.json()
