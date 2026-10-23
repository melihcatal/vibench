from identity_client import build_authorize_url, generate_pkce_pair, get_cognito_config
from identity_models import OAuthLoginRequest


def pkce_login(state: str | None = None) -> dict:
    cfg = get_cognito_config()
    pkce = generate_pkce_pair()
    login = OAuthLoginRequest(
        client_id=cfg["client_id"],
        redirect_uri=cfg["redirect_uri"],
        state=state,
        code_challenge=pkce["code_challenge"],
        code_challenge_method="S256",
    )
    return {"authorization_url": build_authorize_url(login), "code_verifier": pkce["code_verifier"]}
