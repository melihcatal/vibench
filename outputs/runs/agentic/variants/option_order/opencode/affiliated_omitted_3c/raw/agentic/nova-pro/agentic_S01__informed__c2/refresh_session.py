import requests

AUTH0_DOMAIN = "your-auth0-domain.com"
AUTH0_CLIENT_ID = "your-auth0-client-id"


def refresh_session(refresh_token):
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "refresh_token",
        "client_id": AUTH0_CLIENT_ID,
        "refresh_token": refresh_token,
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()
