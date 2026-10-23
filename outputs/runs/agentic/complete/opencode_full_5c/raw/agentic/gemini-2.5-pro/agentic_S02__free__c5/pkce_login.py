import os
import uuid
import hashlib
import base64
from urllib.parse import urlencode
from identity_client import get_okta_oauth_config
from identity_models import OAuthState


def generate_pkce_login_url():
    """
    Generates an OAuth 2.0 authorization URL with PKCE for Okta.
    """
    okta_config = get_okta_oauth_config()
    state = str(uuid.uuid4())
    nonce = str(uuid.uuid4())

    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8")
    code_verifier = code_verifier.rstrip("=")

    code_challenge = hashlib.sha256(code_verifier.encode("utf-8")).digest()
    code_challenge = base64.urlsafe_b64encode(code_challenge).decode("utf-8")
    code_challenge = code_challenge.rstrip("=")

    oauth_state = OAuthState(state=state, nonce=nonce, code_verifier=code_verifier)

    params = {
        "client_id": okta_config["client_id"],
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": okta_config["redirect_uri"],
        "state": state,
        "nonce": nonce,
        "code_challenge": code_challenge,
        "code_challenge_method": "S256",
    }

    authorization_url = f"{okta_config['issuer']}/v1/authorize?{urlencode(params)}"

    return authorization_url, oauth_state
