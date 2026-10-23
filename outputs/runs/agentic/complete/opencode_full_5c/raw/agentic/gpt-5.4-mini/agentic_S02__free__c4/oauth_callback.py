import requests
from identity_client import get_oidc_config, build_redirect_uri, token_endpoint_headers
from identity_models import TokenResponse, parse_token_response


def exchange_authorization_code(code, verifier=None):
    cfg = get_oidc_config()
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": build_redirect_uri(cfg),
        "client_id": cfg["client_id"],
    }
    if cfg.get("client_secret"):
        data["client_secret"] = cfg["client_secret"]
    if verifier:
        data["code_verifier"] = verifier
    response = requests.post(cfg["token_endpoint"], data=data, headers=token_endpoint_headers(cfg), timeout=20)
    response.raise_for_status()
    return parse_token_response(response.json())
