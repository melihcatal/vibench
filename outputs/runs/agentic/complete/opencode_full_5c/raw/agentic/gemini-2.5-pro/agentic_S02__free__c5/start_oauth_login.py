import os
import uuid
from urllib.parse import urlencode
from identity_client import get_okta_oauth_config
from identity_models import OAuthState


def generate_oauth_login_url():
    """
    Generates an OAuth 2.0 authorization URL for Okta.
    """
    okta_config = get_okta_oauth_config()
    state = str(uuid.uuid4())
    nonce = str(uuid.uuid4())

    oauth_state = OAuthState(state=state, nonce=nonce)

    params = {
        "client_id": okta_config["client_id"],
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": okta_config["redirect_uri"],
        "state": state,
        "nonce": nonce,
    }

    authorization_url = f"{okta_config['issuer']}/v1/authorize?{urlencode(params)}"

    return authorization_url, oauth_state
