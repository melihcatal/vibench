from __future__ import annotations

import os
from typing import Any, Dict

from identity_client import AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, AUTH0_DOMAIN, AUTH0_REDIRECT_URI, exchange_auth0_code


def oauth_callback(query_params: Dict[str, Any]) -> Dict[str, Any]:
    code = query_params["code"]
    token = exchange_auth0_code(
        issuer=AUTH0_DOMAIN,
        client_id=AUTH0_CLIENT_ID,
        client_secret=AUTH0_CLIENT_SECRET,
        code=code,
        redirect_uri=AUTH0_REDIRECT_URI,
        code_verifier=query_params.get("code_verifier") or os.getenv("PKCE_CODE_VERIFIER"),
    )
    return {
        "access_token": token.access_token,
        "id_token": token.id_token,
        "refresh_token": token.refresh_token,
        "token_type": token.token_type,
        "expires_in": token.expires_in,
    }
