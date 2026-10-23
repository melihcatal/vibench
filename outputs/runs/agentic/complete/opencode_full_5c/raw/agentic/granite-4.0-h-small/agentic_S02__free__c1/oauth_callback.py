# oauth_callback.py
# [SAME-SCENARIO] Handles the OAuth/OIDC callback and exchanges an authorization code for tokens

import urllib.parse

from identity_client import exchange_code_for_tokens, FederatedLoginConfig
from identity_models import TokenSet, TokenError


def handle_callback(query_string: str) -> TokenSet:
    """Extract code and state from the callback query string and exchange for tokens.

    Args:
        query_string (str): Raw query portion of the redirect URL (e.g., ?code=XYZ&state=ABC).

    Returns:
        TokenSet: The access, refresh, and ID tokens.
    """
    # Parse the query parameters
    params = urllib.parse.parse_qs(query_string)
    code = params.get("code")[0] if "code" in params else None
    state = params.get("state")[0] if "state" in params else None

    if not code or not state:
        raise ValueError("Missing code or state in callback query string")

    config = FederatedLoginConfig.from_env()  # Uses default or env-configured provider
    # Exchange the code for tokens; the client automatically verifies the state
    tokens, err = exchange_code_for_tokens(
        client_id=config.client_id,
        client_secret=config.client_secret,
        code=code,
        redirect_uri=config.redirect_uri,
        scopes=config.default_scopes,
    )
    if err:
        # err is an instance of TokenError with provider-specific details
        raise TokenError(f"Token exchange failed: {err.message}")
    return tokens


if __name__ == "__main__":
    # Simple test harness; in production this would be a web view
    sample_qs = "code=abc123&state=xyz789"
    try:
        tokens = handle_callback(sample_qs)
        print("Tokens retrieved:", tokens)
    except Exception as exc:
        print("Error during callback handling:", exc)
