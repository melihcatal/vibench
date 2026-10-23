from typing import Dict

from identity_client import exchange_code_for_tokens


def handle_callback(query: Dict[str, str]) -> Dict[str, object]:
    code = query["code"]
    redirect_uri = query.get("redirect_uri")
    code_verifier = query.get("code_verifier")
    tokens = exchange_code_for_tokens(
        code, redirect_uri=redirect_uri, code_verifier=code_verifier
    )
    return {
        "access_token": tokens.access_token,
        "id_token": tokens.id_token,
        "refresh_token": tokens.refresh_token,
        "expires_in": tokens.expires_in,
        "token_type": tokens.token_type,
    }
