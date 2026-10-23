import requests


def register_user(email, password):
    url = "https://api.auth0.com/dbconnections/signup"
    headers = {"Content-Type": "application/json"}
    data = {
        "email": email,
        "password": password,
        "connection": "Username-Password-Authentication",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
