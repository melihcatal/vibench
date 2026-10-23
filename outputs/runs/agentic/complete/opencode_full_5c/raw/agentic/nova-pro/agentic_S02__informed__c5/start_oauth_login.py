import os
import requests

AUTH0_DOMAIN = os.getenv("AUTH0_DOMAIN")
AUTH0_CLIENT_ID = os.getenv("AUTH0_CLIENT_ID")


def start_oauth_login():
    auth_url = f"https://{AUTH0_DOMAIN}/authorize?response_type=code&client_id={AUTH0_CLIENT_ID}&redirect_uri=http://localhost:3000/callback&scope=openid%20profile&state=xyz"
    print(f"Redirect to: {auth_url}")
    return auth_url
