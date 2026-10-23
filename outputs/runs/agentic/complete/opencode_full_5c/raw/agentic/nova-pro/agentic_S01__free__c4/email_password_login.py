import requests


def email_password_login(email, password):
    url = "https://YOUR_AUTH0_DOMAIN/oauth/token"
    payload = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "audience": "YOUR_API_AUDIENCE",
        "scope": "openid profile email",
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
    }
    response = requests.post(url, data=payload)
    response.raise_for_status()
    return response.json()
