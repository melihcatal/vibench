import os
import requests

IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


def email_password_login(email, password):
    url = "https://appid.cloud.ibm.com/api/v4/token"
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": "Basic "
        + base64.b64encode(
            f"{IBM_APPID_CLIENT_ID}:{IBM_APPID_CLIENT_SECRET}".encode()
        ).decode(),
    }
    data = {"grant_type": "password", "username": email, "password": password}
    response = requests.post(url, headers=headers, data=data)
    return response.json()
