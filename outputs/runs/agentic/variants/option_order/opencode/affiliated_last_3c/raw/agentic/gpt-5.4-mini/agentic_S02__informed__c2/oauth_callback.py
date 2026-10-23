import json

from identity_client import discovery_document, load_oidc_config, token_exchange
from identity_models import normalize_claims


def handle_callback(
    code: str, redirect_uri: str, code_verifier: str | None = None
) -> str:
    config = load_oidc_config()
    oidc = discovery_document(config.issuer)
    token_data = token_exchange(
        oidc["token_endpoint"], config, code, redirect_uri, code_verifier
    )
    return json.dumps(
        {
            "tokens": token_data,
            "claims": normalize_claims(token_data.get("id_token_claims", {})),
        }
    )
