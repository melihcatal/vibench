from typing import Dict

from identity_client import exchange_code_for_tokens, load_config
from identity_models import TokenResponse


def handle_oauth_callback(query: Dict[str, str]) -> TokenResponse:
    code = query["code"]
    config = load_config()
    return exchange_code_for_tokens(
        config,
        code,
        redirect_uri=query.get("redirect_uri"),
        code_verifier=query.get("code_verifier"),
    )
