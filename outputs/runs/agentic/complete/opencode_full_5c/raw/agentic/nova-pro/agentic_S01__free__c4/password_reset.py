import requests


def start_password_reset(email):
    url = "https://YOUR_AUTH0_DOMAIN/dbconnections/change_password"
    payload = {"email": email, "connection": "Username-Password-Authentication"}
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()
