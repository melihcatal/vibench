import os
import urllib.parse
from identity_client import get_auth0_config

def start_auth0_login_flow():
    config = get_auth0_config()
    domain = config["AUTH0_DOMAIN"]
    client_id = config["AUTH0_CLIENT_ID"]
    redirect_uri = config["AUTH0_REDIRECT_URI"]
    scope = "openid profile email"
    response_type = "code"

    auth_url = (
        f"https://{domain}/authorize?"
        f"response_type={response_type}&"
        f"client_id={client_id}&"
        f"redirect_uri={urllib.parse.quote_plus(redirect_uri)}&"
        f"scope={urllib.parse.quote_plus(scope)}"
    )
    print(f"Redirect to: {auth_url}")
    return auth_url

if __name__ == "__main__":
    start_auth0_login_flow()
