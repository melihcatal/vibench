import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

import auth0


def oauth_callback(code):
    # Auth0 OAuth callback and token exchange
    pass
