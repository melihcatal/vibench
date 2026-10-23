from identity_client import build_authorize_url, load_identity_config
from identity_models import LoginRequest


def start_oauth_login(state: str, scopes=None, redirect_uri: str = ""):
    config = load_identity_config()
    request = LoginRequest(
        redirect_uri=redirect_uri or config["redirect_uri"],
        state=state,
        scope=scopes or ["openid", "email", "profile"],
    )
    return {"authorization_url": build_authorize_url(config, request), "provider": "AWS Cognito", "request": request}
