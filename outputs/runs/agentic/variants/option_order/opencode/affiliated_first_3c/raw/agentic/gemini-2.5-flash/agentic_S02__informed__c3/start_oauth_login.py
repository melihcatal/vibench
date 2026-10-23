import os
import uuid
from identity_client import get_auth0_config, build_auth0_authorize_url


def start_oauth_login():
    config = get_auth0_config()
    if not config["DOMAIN"] or not config["CLIENT_ID"] or not config["CALLBACK_URL"]:
        raise ValueError("Auth0 configuration environment variables are not set.")

    state = str(uuid.uuid4())
    os.environ["OAUTH_STATE"] = state  # In a real app, use a secure session store

    authorization_url = build_auth0_authorize_url(config, state)
    print(f"Redirect to: {authorization_url}")
    return authorization_url


if __name__ == "__main__":
    # Example usage: In a web framework, you would return a redirect response
    # For this example, we just print the URL.
    login_url = start_oauth_login()
    print(
        f"Please open this URL in your browser to start the login process:\n{login_url}"
    )
