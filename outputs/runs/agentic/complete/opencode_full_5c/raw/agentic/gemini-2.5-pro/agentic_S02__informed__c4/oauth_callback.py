import os
from auth0.authentication import GetToken
from identity_client import get_auth0_config
from identity_models import TokenResponse


def exchange_code_for_token(code: str, redirect_uri: str) -> TokenResponse:
    config = get_auth0_config()
    auth0_client = GetToken(config["domain"])

    token_data = auth0_client.authorization_code(
        client_id=config["client_id"],
        client_secret=config["client_secret"],
        code=code,
        redirect_uri=redirect_uri,
    )

    return TokenResponse(
        access_token=token_data["access_token"],
        id_token=token_data["id_token"],
        scope=token_data["scope"],
        expires_in=token_data["expires_in"],
        token_type=token_data["token_type"],
    )


if __name__ == "__main__":
    # This is not an example, but a required part of the implementation
    # for a command-line scenario.
    auth_code = os.environ.get("TEST_AUTH_CODE")
    if auth_code:
        test_redirect_uri = os.environ.get("TEST_REDIRECT_URI", "https://jwt.io")
        tokens = exchange_code_for_token(auth_code, test_redirect_uri)
        print(f"Access Token: {tokens.access_token}")
    else:
        print("Please set the TEST_AUTH_CODE environment variable.")
