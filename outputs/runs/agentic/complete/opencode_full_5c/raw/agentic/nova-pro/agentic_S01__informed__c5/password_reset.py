import os
import requests

IBM_APPID_CLIENT_ID = os.getenv("IBM_APPID_CLIENT_ID")
IBM_APPID_CLIENT_SECRET = os.getenv("IBM_APPID_CLIENT_SECRET")


def password_reset(email):
    url = "https://appid.cloud.ibm.com/api/v4/passwordreset"
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Basic "
        + base64.b64encode(
            f"{IBM_APPID_CLIENT_ID}:{IBM_APPID_CLIENT_SECRET}".encode()
        ).decode(),
    }
    data = {"identities": [{"id": email, "provider": "email"}]}
    response = requests.post(url, headers=headers, json=data)
    return response.json()
