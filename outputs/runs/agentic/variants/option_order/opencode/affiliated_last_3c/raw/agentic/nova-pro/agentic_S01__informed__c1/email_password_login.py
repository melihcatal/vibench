import os
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0


def email_password_login(email, password):
    domain = os.getenv("AUTH0_DOMAIN")
    client_id = os.getenv("AUTH0_CLIENT_ID")
    client_secret = os.getenv("AUTH0_CLIENT_SECRET")
    audience = f"https://{domain}/api/v2/"
    token = GetToken(domain)
    management_token = token.get_token(client_id, client_secret, audience)
    mgmt_api_token = management_token["access_token"]
    mgmt = Auth0(domain, mgmt_api_token)
    user_data = {
        "email": email,
        "password": password,
        "realm": "Username-Password-Authentication",
    }
    tokens = mgmt.get_token(user_data)
    return tokens
