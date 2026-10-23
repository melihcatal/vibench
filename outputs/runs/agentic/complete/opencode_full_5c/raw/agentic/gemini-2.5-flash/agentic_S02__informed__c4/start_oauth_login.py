import os
from urllib.parse import quote_plus, urlencode

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CALLBACK_URL = os.getenv("AUTH0_CALLBACK_URL")


def get_auth0_login_url():
    """Constructs the Auth0 login URL for the authorization code flow."""
    return f"https://{AUTH0_DOMAIN}/authorize?" + urlencode(
        {
            "response_type": "code",
            "client_id": AUTH0_CLIENT_ID,
            "redirect_uri": AUTH0_CALLBACK_URL,
            "scope": "openid profile email",
        }
    )


if __name__ == "__main__":
    print(f"Auth0 Login URL: {get_auth0_login_url()}")
