import requests


def register_user(email, password):
    url = "https://YOUR_AUTH0_DOMAIN/dbconnections/signup"
    payload = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
