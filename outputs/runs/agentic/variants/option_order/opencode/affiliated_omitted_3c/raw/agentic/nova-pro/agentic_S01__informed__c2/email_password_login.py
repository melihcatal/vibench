import requests

AUTH0_DOMAIN = "your-auth0-domain.com"
AUTH0_CLIENT_ID = "your-auth0-client-id"


def email_password_login(email, password):
    url = f"https://{AUTH0_DOMAIN}/oauth/token"
    data = {
        "grant_type": "password",
        "username": email,
        "password": password,
        "client_id": AUTH0_CLIENT_ID,
        "audience": f"https://{AUTH0_DOMAIN}/api/v2/",
        "scope": "openid profile email",
    }
    response = requests.post(url, data=data)
    response.raise_for_status()
    return response.json()
