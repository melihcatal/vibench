import requests


def refresh_session(refresh_token):
    url = "https://api.auth0.com/oauth/token"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "refresh_token",
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "refresh_token": refresh_token,
        "audience": "https://YOUR_API_IDENTIFIER",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
