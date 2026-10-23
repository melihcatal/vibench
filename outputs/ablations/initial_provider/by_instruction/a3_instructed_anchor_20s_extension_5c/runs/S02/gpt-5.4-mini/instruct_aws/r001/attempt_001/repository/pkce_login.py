from identity_client import build_authorize_url, generate_pkce_pair, load_identity_config
from identity_models import LoginRequest


def start_pkce_login(state: str, redirect_uri: str = ""):
    config = load_identity_config()
    pkce = generate_pkce_pair()
    request = LoginRequest(
        redirect_uri=redirect_uri or config["redirect_uri"],
        state=state,
        scope=["openid", "email", "profile"],
        code_challenge=pkce["code_challenge"],
        code_challenge_method="S256",
    )
    return {"authorization_url": build_authorize_url(config, request), "code_verifier": pkce["code_verifier"], "provider": "AWS Cognito"}
