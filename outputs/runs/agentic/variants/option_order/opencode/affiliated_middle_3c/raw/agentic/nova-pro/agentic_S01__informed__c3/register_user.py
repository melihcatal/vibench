import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0

# Configuration
AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")
AUTH0_CLIENT_SECRET = os.getenv("AUTH0_CLIENT_SECRET")

# Auth0 Management API client
mgmt_api_token = GetToken(AUTH0_DOMAIN).client_credentials(
    AUTH0_CLIENT_ID, AUTH0_CLIENT_SECRET, "https://{}/".format(AUTH0_DOMAIN)
)
mgmt_api_token = mgmt_api_token["access_token"]
auth0 = Auth0(AUTH0_DOMAIN, mgmt_api_token)


def register_user(email, password):
    user_data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
    }
    user = auth0.users.create(user_data)
    return user
