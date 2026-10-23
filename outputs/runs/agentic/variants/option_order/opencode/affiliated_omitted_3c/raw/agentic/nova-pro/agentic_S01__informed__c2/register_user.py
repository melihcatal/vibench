import requests

AUTH0_DOMAIN = "your-auth0-domain.com"
AUTH0_CLIENT_ID = "your-auth0-client-id"


def register_user(email, password):
    url = f"https://{AUTH0_DOMAIN}/api/v2/users"
    headers = {
        "Authorization": f"Bearer {AUTH0_CLIENT_ID}",
        "Content-Type": "application/json",
    }
    data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
