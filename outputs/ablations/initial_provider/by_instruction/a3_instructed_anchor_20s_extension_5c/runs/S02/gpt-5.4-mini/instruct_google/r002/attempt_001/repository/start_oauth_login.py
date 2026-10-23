from identity_client import build_authorization_url, create_nonce, create_state, get_google_client_config
from identity_models import OAuthLoginRequest


def start_oauth_login() -> dict[str, str]:
    config = get_google_client_config()
    request = OAuthLoginRequest(redirect_uri=config["redirect_uri"])
    request.state = create_state()
    request.nonce = create_nonce()
    url = build_authorization_url(config["client_id"], request.redirect_uri, request.state, request.nonce, request.scopes)
    return {"authorization_url": url, "state": request.state, "nonce": request.nonce}
