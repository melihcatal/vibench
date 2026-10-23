import os
import requests

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")


def start_oauth_login():
    authorization_url = f"{COGNITO_DOMAIN}/login?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=openid+profile+email"
    print(f"Authorization URL: {authorization_url}")
    return authorization_url
