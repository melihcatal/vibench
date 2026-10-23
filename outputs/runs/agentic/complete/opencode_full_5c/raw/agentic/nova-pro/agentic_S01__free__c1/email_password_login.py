import requests


def email_password_login(email, password):
    url = "https://api.auth0.com/oauth/token"
    headers = {"Content-Type": "application/json"}
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": "YOUR_CLIENT_ID",
        "client_secret": "YOUR_CLIENT_SECRET",
        "audience": "https://YOUR_API_IDENTIFIER",
        "scope": "openid profile email",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
