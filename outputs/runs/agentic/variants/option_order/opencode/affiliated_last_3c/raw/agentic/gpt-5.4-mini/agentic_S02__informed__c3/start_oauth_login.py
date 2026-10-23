from identity_client import load_identity_config, make_state
from identity_models import OAuthLoginRequest


def build_authorization_url(redirect_uri: str) -> str:
    config = load_identity_config()
    request = OAuthLoginRequest(state=make_state(), redirect_uri=redirect_uri)
    return (
        f"{config['authorization_endpoint']}?response_type=code&client_id={config['client_id']}"
        f"&redirect_uri={request.redirect_uri}&scope={request.scope}&state={request.state}"
    )
