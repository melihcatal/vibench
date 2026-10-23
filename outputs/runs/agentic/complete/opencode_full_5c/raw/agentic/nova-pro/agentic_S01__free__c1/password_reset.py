import requests


def password_reset(email):
    url = "https://api.auth0.com/dbconnections/change_password"
    headers = {"Content-Type": "application/json"}
    data = {
        "client_id": "YOUR_CLIENT_ID",
        "email": email,
        "connection": "Username-Password-Authentication",
    }
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()
