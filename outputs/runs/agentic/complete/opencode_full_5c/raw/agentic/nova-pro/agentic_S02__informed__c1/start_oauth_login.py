import os
import requests

COGNITO_DOMAIN = os.getenv("COGNITO_DOMAIN")
COGNITO_CLIENT_ID = os.getenv("COGNITO_CLIENT_ID")


def start_oauth_login():
    authorize_url = f"https://{COGNITO_DOMAIN}/oauth2/authorize?client_id={COGNITO_CLIENT_ID}&response_type=code&scope=openid+profile+email"
    print(f"Redirect to: {authorize_url}")
    # Redirect user to authorize_url
