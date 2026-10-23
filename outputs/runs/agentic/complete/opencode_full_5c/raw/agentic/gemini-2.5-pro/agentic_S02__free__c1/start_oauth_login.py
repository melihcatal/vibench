import os
from urllib.parse import urlencode
from identity_client import IdentityClientConfig


def get_okta_auth_url():
    config = IdentityClientConfig()
    params = {
        "client_id": config.OKTA_CLIENT_ID,
        "response_type": "code",
        "scope": "openid profile email",
        "redirect_uri": config.OKTA_REDIRECT_URI,
        "state": "random_state_string",
    }

    authorization_url = (
        f"https://{config.OKTA_DOMAIN}/oauth2/default/v1/authorize?{urlencode(params)}"
    )
    return authorization_url


if __name__ == "__main__":
    print(f"Login URL: {get_okta_auth_url()}")
