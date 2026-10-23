import os
from identity_models import OAuthConfig, TokenResponse
from identity_client import load_oauth_config, exchange_code_for_tokens


def handle_oauth_callback(
    authorization_code: str,
    expected_state: str | None = None,
    received_state: str | None = None,
    config: OAuthConfig | None = None,
) -> dict:
    if expected_state and received_state and expected_state != received_state:
        raise ValueError("State mismatch: possible CSRF attack detected")

    if config is None:
        config = load_oauth_config()

    if not authorization_code:
        raise ValueError("Authorization code is required")

    token_response: TokenResponse = exchange_code_for_tokens(
        config=config,
        authorization_code=authorization_code,
    )

    if not token_response.is_valid:
        raise ValueError("Token exchange failed: invalid token response")

    return {
        "access_token": token_response.access_token,
        "id_token": token_response.id_token,
        "refresh_token": token_response.refresh_token,
        "token_type": token_response.token_type,
        "expires_in": token_response.expires_in,
        "scope": token_response.scope,
        "provider": "auth0",
        "domain": config.domain,
    }


def exchange_code(
    authorization_code: str,
    config: OAuthConfig | None = None,
) -> TokenResponse:
    if config is None:
        config = load_oauth_config()
    return exchange_code_for_tokens(
        config=config,
        authorization_code=authorization_code,
    )


if __name__ == "__main__":
    code = os.getenv("AUTHORIZATION_CODE", "")
    if code:
        result = handle_oauth_callback(authorization_code=code)
        print(f"Access token obtained: {bool(result['access_token'])}")
        print(f"Provider: {result['provider']}")
