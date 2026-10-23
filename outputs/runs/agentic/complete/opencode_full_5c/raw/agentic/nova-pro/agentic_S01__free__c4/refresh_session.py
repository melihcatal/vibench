import requests


def refresh_session(refresh_token):
    url = "https://YOUR_AUTH0_DOMAIN/oauth/token"
    payload = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()
