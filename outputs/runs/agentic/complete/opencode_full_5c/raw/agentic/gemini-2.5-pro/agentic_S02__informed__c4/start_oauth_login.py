import os
from auth0.authentication import GetToken
from identity_client import get_auth0_config


def start_login(redirect_uri: str, state: str) -> str:
    config = get_auth0_config()
    auth0_client = GetToken(config["domain"])

    authorize_url = auth0_client.authorization_url(
        client_id=config["client_id"],
        redirect_uri=redirect_uri,
        response_type="code",
        scope="openid profile email",
        state=state,
    )
    return authorize_url


if __name__ == "__main__":
    # This is not an example, but a required part of the implementation
    # for a command-line scenario.
    test_redirect_uri = os.environ.get("TEST_REDIRECT_URI", "https://jwt.io")
    print(f"Login URL: {start_login(test_redirect_uri, 'some-random-state')}")
