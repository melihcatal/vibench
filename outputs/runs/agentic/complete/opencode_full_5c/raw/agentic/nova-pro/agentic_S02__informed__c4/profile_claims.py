import os

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")

import auth0


def profile_claims(access_token):
    # Auth0 profile claims fetching
    pass
