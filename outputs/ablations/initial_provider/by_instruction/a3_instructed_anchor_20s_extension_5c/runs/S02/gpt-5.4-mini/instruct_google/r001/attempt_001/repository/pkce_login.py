from urllib.parse import urlencode

from identity_client import GOOGLE_AUTH_ENDPOINT, load_identity_config, new_code_verifier, pkce_challenge, new_state


def pkce_login(scope: str = "openid email profile"):
    config = load_identity_config()
    verifier = new_code_verifier()
    challenge = pkce_challenge(verifier)
    state = new_state()
    params = {
        "client_id": config["google_client_id"],
        "redirect_uri": config["google_redirect_uri"],
        "response_type": "code",
        "scope": scope,
        "state": state,
        "code_challenge": challenge,
        "code_challenge_method": "S256",
    }
    return f"{GOOGLE_AUTH_ENDPOINT}?{urlencode(params)}", verifier, state
