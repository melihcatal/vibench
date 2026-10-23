import os
import uuid
from identity_client import MicrosoftEntraIdentityClient
from identity_models import OAuthState, PKCEData
import hashlib
import base64


def generate_pkce_data() -> PKCEData:
    code_verifier = base64.urlsafe_b64encode(os.urandom(40)).decode("utf-8").rstrip("=")
    code_challenge = (
        base64.urlsafe_b64encode(hashlib.sha256(code_verifier.encode("utf-8")).digest())
        .decode("utf-8")
        .rstrip("=")
    )
    return PKCEData(code_verifier=code_verifier, code_challenge=code_challenge)


def start_oauth_login(redirect_uri: str) -> dict:
    client = MicrosoftEntraIdentityClient()
    state = str(uuid.uuid4())
    pkce_data = generate_pkce_data()

    auth_url = client.get_auth_url(
        redirect_uri=redirect_uri,
        state=state,
        code_challenge=pkce_data.code_challenge,
        code_challenge_method=pkce_data.code_challenge_method,
    )

    oauth_state = OAuthState(
        state=state, redirect_uri=redirect_uri, pkce_data=pkce_data
    )

    return {
        "auth_url": auth_url,
        "state": oauth_state.state,
        "code_verifier": pkce_data.code_verifier,
    }
