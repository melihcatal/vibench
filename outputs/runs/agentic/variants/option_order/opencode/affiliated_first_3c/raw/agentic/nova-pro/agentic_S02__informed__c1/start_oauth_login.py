import os
import requests

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")


def start_oauth_login():
    auth_url = f"{COGNITO_DOMAIN}/oauth2/authorize?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=openid+profile+email"
    print(f"Redirect to: {auth_url}")
    return auth_url
