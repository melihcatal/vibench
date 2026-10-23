from identity_client import build_authorize_url, get_cognito_config
from identity_models import OAuthLoginRequest


def start_oauth_login(state: str | None = None) -> dict:
    cfg = get_cognito_config()
    login = OAuthLoginRequest(
        client_id=cfg["client_id"],
        redirect_uri=cfg["redirect_uri"],
        state=state,
    )
    return {"authorization_url": build_authorize_url(login)}
