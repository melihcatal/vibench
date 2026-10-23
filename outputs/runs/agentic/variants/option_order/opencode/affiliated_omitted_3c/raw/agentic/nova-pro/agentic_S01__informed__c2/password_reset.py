import requests

AUTH0_DOMAIN = "your-auth0-domain.com"
AUTH0_CLIENT_ID = "your-auth0-client-id"


def password_reset(email):
    url = f"https://{AUTH0_DOMAIN}/dbconnections/change_password"
    headers = {
        "Authorization": f"Bearer {AUTH0_CLIENT_ID}",
        "Content-Type": "application/json",
    }
    data = {"client_id": AUTH0_CLIENT_ID, "email": email}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
