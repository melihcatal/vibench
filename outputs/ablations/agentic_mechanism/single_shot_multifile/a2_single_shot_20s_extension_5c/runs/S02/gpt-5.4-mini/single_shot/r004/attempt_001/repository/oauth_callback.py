import os
from dataclasses import asdict

import requests

from identity_client import build_oidc_config, verify_state_payload
from identity_models import TokenExchangeRequest, TokenExchangeResponse

TOKEN_ENDPOINT_OVERRIDE = os.environ.get("IDP_TOKEN_ENDPOINT", "")


def exchange_authorization_code(code: str, state: str, redirect_uri: str, code_verifier: str | None = None) -> TokenExchangeResponse:
    cfg = build_oidc_config()
    verify_state_payload(state)
    token_endpoint = TOKEN_ENDPOINT_OVERRIDE or cfg.token_endpoint()
    req = TokenExchangeRequest(
        client_id=cfg.client_id,
        client_secret=cfg.client_secret,
        code=code,
        redirect_uri=redirect_uri,
        grant_type="authorization_code",
        code_verifier=code_verifier,
        scope=cfg.scopes,
    )
    payload = {k: v for k, v in asdict(req).items() if v is not None and v != ""}
    response = requests.post(token_endpoint, data=payload, timeout=15)
    response.raise_for_status()
    data = response.json()
    return TokenExchangeResponse.from_provider_json(data)


def callback_result(code: str, state: str, redirect_uri: str, code_verifier: str | None = None) -> dict:
    tokens = exchange_authorization_code(code, state, redirect_uri, code_verifier=code_verifier)
    return tokens.to_dict()
