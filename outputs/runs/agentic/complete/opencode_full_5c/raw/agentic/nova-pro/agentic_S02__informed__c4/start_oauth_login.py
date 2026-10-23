import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

import auth0


def start_oauth_login():
    # Auth0 OAuth login initiation
    pass
