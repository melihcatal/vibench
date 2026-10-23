import os
import requests
from dotenv import load_dotenv

load_dotenv()

AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
REDIRECT_URI = 'http://localhost:5000/callback'

def start_oauth_login():
    # Build the authorization URL for the Auth0 Authorization Code flow
    base_url = f'https://{AUTH0_DOMAIN}'
    authorize_url = (
        f"{base_url}/authorize?"
        f"response_type=code&"
        f"client_id={AUTH0_CLIENT_ID}&"
        f"redirect_uri={REDIRECT_URI}&"
        f"scope=openid%20profile%20email&"
        f"state={os.urllib.parse.quote(str(uuid.uuid4()))}&"
        f"nonce={os.urllib.parse.quote(str(uuid.uuid4()))}"
    )
    print("Open this URL in your browser:")
    print(authorize_url)

if __name__ == "__main__":
    start_oauth_login()